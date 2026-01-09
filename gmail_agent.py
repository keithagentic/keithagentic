#!/usr/bin/env python3
"""Summarize Gmail messages about AI agents into an X post."""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from openai import OpenAI

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
DEFAULT_QUERY = "(agent OR agents OR agentic OR autonomous) newer_than:14d"
DEFAULT_MODEL = "gpt-4o-mini"
KEYWORDS = (
    "agent",
    "agents",
    "agentic",
    "autonomous",
    "tooling",
    "workflow",
    "multi-agent",
    "llm",
    "reasoning",
)


@dataclass
class MessageSummary:
    subject: str
    snippet: str
    from_address: str


def load_credentials(credentials_path: Path, token_path: Path) -> Credentials:
    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_path.write_text(creds.to_json())
        return creds
    flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
    creds = flow.run_local_server(port=0)
    token_path.write_text(creds.to_json())
    return creds


def build_gmail_service(credentials_path: Path, token_path: Path):
    creds = load_credentials(credentials_path, token_path)
    return build("gmail", "v1", credentials=creds)


def extract_headers(payload: dict, header_name: str) -> str:
    for header in payload.get("headers", []):
        if header.get("name", "").lower() == header_name.lower():
            return header.get("value", "").strip()
    return ""


def fetch_messages(service, query: str, max_results: int) -> list[MessageSummary]:
    response = (
        service.users()
        .messages()
        .list(userId="me", q=query, maxResults=max_results)
        .execute()
    )
    message_ids = response.get("messages", [])
    summaries: list[MessageSummary] = []
    for message in message_ids:
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=message["id"], format="metadata")
            .execute()
        )
        payload = msg.get("payload", {})
        subject = extract_headers(payload, "Subject") or "(No subject)"
        from_address = extract_headers(payload, "From")
        snippet = msg.get("snippet", "")
        summaries.append(
            MessageSummary(subject=subject, snippet=snippet, from_address=from_address)
        )
    return summaries


def filter_messages(messages: Iterable[MessageSummary]) -> list[MessageSummary]:
    filtered: list[MessageSummary] = []
    for message in messages:
        haystack = f"{message.subject} {message.snippet}".lower()
        if any(keyword in haystack for keyword in KEYWORDS):
            filtered.append(message)
    return filtered


def build_prompt(messages: Iterable[MessageSummary]) -> str:
    lines = [
        "You are a helpful assistant that summarizes inbox updates.",
        "Create a single X post with exactly 5 interesting developments in the AI agents space.",
        "Use numbered points 1-5. Keep the post under 280 characters.",
        "If there are fewer than 5 clear developments, synthesize from what is available.",
        "Avoid fabricating facts; only use provided snippets.",
        "",
        "Inbox highlights:",
    ]
    for message in messages:
        lines.append(
            f"- Subject: {message.subject} | From: {message.from_address} | Snippet: {message.snippet}"
        )
    return "\n".join(lines)


def generate_x_post(prompt: str, model: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is not set.")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize Gmail messages into a 5-point X post about agents."
    )
    parser.add_argument(
        "--credentials",
        type=Path,
        default=Path("credentials.json"),
        help="Path to OAuth client credentials JSON.",
    )
    parser.add_argument(
        "--token",
        type=Path,
        default=Path("token.json"),
        help="Path to OAuth token cache.",
    )
    parser.add_argument(
        "--query",
        type=str,
        default=DEFAULT_QUERY,
        help="Gmail search query.",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=30,
        help="Max number of messages to scan.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help="OpenAI model name.",
    )
    parser.add_argument(
        "--no-filter",
        action="store_true",
        help="Disable keyword filtering.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.credentials.exists():
        raise SystemExit(
            f"Missing credentials file: {args.credentials}. See README.md for setup."
        )
    service = build_gmail_service(args.credentials, args.token)
    messages = fetch_messages(service, args.query, args.max_results)
    if not args.no_filter:
        messages = filter_messages(messages)
    if not messages:
        raise SystemExit("No matching messages found.")
    prompt = build_prompt(messages)
    x_post = generate_x_post(prompt, args.model)
    print(x_post)


if __name__ == "__main__":
    main()
