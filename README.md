## Hey there!

### About me
- 🔭 I’m currently working on GenAI for enterprise IT and product management.
- 🌱 I’m currently learning about GitHub and about all things AI and Agentic.
- 👯 I’m looking to collaborate on ways product managers are using AI, and ways enterprise IT is using AI.
- 🤔 I’m looking for help with applying Agentic tools to product management and enterprise IT.
- 💬 Ask me about product management and enterprise IT.
- 📫 How to reach me: keith.agentic@gmail.com or 801.580.8065
- ⚡ Fun fact: I ski, hike, mountain bike, and trail run for fun.

## Gmail Agent Summarizer

This script pulls recent Gmail messages related to AI agents and produces a single X-ready post with 5 numbered developments.

### Setup
1. Create a Google Cloud project and enable the Gmail API.
2. Download OAuth client credentials and save as `credentials.json` in this repo.
3. Install dependencies:
   ```bash
   python -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib openai
   ```
4. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-key"
   ```

### Usage
```bash
python gmail_agent.py --query "(agent OR agents OR agentic OR autonomous) newer_than:14d"
```

Optional flags:
- `--max-results 50` to scan more messages.
- `--no-filter` to skip keyword filtering.
- `--model gpt-4o-mini` to change the OpenAI model.

The first run opens a browser for OAuth consent and stores a token in `token.json`.
