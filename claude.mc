# CLAUDE.md - Hearing Heroes Project Guide

## Project Overview
Hearing Heroes is a speech discrimination game designed for children with hearing impairments, particularly those with cochlear implants. The game focuses on consonant manner contrasts through interactive audio-visual exercises.

## Technical Stack
- TypeScript
- React + PixiJS
- Vite for building
- IndexedDB for data storage
- PWA for offline functionality on iPad

## Commands to Run
- `npm install` - Install dependencies
- `npm run dev` - Start development server
- `npm run build` - Build production version
- `npm run lint` - Run ESLint
- `npm run typecheck` - Run TypeScript type checking
- `npm test` - Run all tests
- `npm run test:watch` - Run tests in watch mode
- `npm run test:coverage` - Run tests with coverage report

## Important Project Areas
1. **Game Mechanics**: Audio prompts with image pairs (e.g., cave/wave)
2. **Progress Tracking**: Metrics stored in IndexedDB
3. **Parent Dashboard**: Protected area with visualizations
4. **Level Progression**: Multiple difficulty levels for consonant contrasts

## Git Branching Strategy
For documenting development progress and enabling others to follow along with the tutorial:

1. Development Phases and Branches:
   - Phase 1: Project Setup - `setup` branch
   - Phase 2: Core Game Mechanics - `game-mechanics` branch
   - Phase 3: Content & Progression - `content-progression` branch
   - Phase 4: Parent Dashboard - `parent-dashboard` branch
   - Phase 5: Testing & Refinement - `refinement` branch

2. Commands for Branch Management:
   - Start new phase: `git checkout -b <branch-name>`
   - Commit changes: `git add . && git commit -m "Description of changes"`
   - Merge to main: `git checkout main && git merge <branch-name>`
   - Tag release: `git tag -a v<version> -m "Phase X complete"`

3. Pull Request Process:
   - Each phase should be completed with a PR to main
   - PRs should include a summary of changes and testing performed

## Testing Strategy

### Testing Framework
- Jest for test runner and assertions
- React Testing Library for component testing
- Test coverage reporting with Jest
- Mock audio functionality for consistent testing

### Types of Tests
1. **Unit Testing**:
   - Individual components and functions
   - Service layer (audio, data storage)
   - Utility functions

2. **Integration Testing**:
   - Game flow and interactions
   - Data persistence with IndexedDB
   - Parent dashboard interactions

3. **Manual Testing**:
   - Focus on real device experience
   - Audio quality and responsiveness
   - Touch interaction validation
   - iPad-specific behavior

### Test Coverage Goals
- Core game mechanics: 90%+ coverage
- Data storage/retrieval: 80%+ coverage
- UI components: 70%+ coverage

### Testing Commands
- `npm test` - Run all tests
- `npm run test:watch` - Run tests in watch mode (development)
- `npm run test:coverage` - Generate coverage reports

## Project References
- Technical specification: `/technical_specification.md`
- Project structure: `/project_structure.md`
- Development phases and git strategy: Technical specification's "Development Phases & Git Strategy" section

## IMPORTANT
- Ignore `prompts.md` this is a non-related file I'm using to keep notes from our conversation.
- DO NOT send or include binary files (*.mp3, *.png, images, audio files, etc.) in your messages. This will cause API errors.
- Use placeholder references or file paths when discussing binary files, never their contents.
