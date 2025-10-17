# TDS Project 1 - LLM Code Deployment

An automated system that receives task requests, generates web applications using LLM, deploys them to GitHub Pages, and handles iterative improvements.

## Overview

This project implements an API endpoint that:
- Receives task requests with app briefs and requirements
- Uses OpenAI GPT-4o to generate complete web applications
- Automatically creates GitHub repositories
- Deploys generated apps to GitHub Pages
- Handles two rounds of development (initial creation + improvements)
- Notifies evaluation servers with deployment details

## Features

- **LLM-Powered Code Generation**: Uses OpenAI GPT-4o to generate HTML/CSS/JS applications
- **Automated GitHub Integration**: Creates repos, commits files, enables Pages
- **Round-Based Development**: Supports initial creation and iterative improvements
- **Attachment Handling**: Processes and includes file attachments in generated apps
- **Duplicate Request Prevention**: Tracks and handles duplicate requests
- **Comprehensive Logging**: Full logging for debugging and monitoring

## Architecture

```
├── app/
│   ├── app.py              # FastAPI main application
│   ├── llm_generator.py    # OpenAI integration for code generation
│   ├── github_utils.py     # GitHub API utilities
│   └── notify.py           # Evaluation server notification
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in repo)
└── README.md              # This file
```

## Setup

### Prerequisites
- Python 3.8+
- OpenAI API key
- GitHub Personal Access Token (with repo permissions)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/tds-project-1.git
cd tds-project-1
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```env
OPENAI_API_KEY=sk-proj-your-key-here
GITHUB_TOKEN=ghp_your-token-here
GITHUB_USERNAME=your-github-username
USER_SECRET=your-secret-key
```

### Running Locally

```bash
python -m app.app
```

Server will start on `http://localhost:7860`

## Usage

### API Endpoints

#### Health Check
```bash
GET /
Response: {"status":"ok","note":"API running"}
```

#### Main Endpoint
```bash
POST /api-endpoint
Content-Type: application/json

{
  "secret": "your-secret",
  "email": "student@example.com",
  "task": "task-id-123",
  "round": 1,
  "nonce": "unique-nonce",
  "brief": "Create a simple todo app",
  "checks": ["Has add button", "Has delete functionality"],
  "evaluation_url": "https://evaluation-server.com/notify",
  "attachments": []
}
```

### Example Request

```bash
curl -X POST http://localhost:7860/api-endpoint \
  -H "Content-Type: application/json" \
  -d '{
    "secret": "your-secret",
    "email": "test@example.com",
    "task": "todo-app-001",
    "round": 1,
    "nonce": "abc123",
    "brief": "Create a todo list app",
    "checks": ["Add tasks", "Delete tasks", "Mark complete"],
    "evaluation_url": "https://httpbin.org/post"
  }'
```

## Deployment

### Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Upload all project files
3. Set environment variables in Space settings
4. Space will auto-deploy

**Live Endpoint:** `https://your-space.hf.space/api-endpoint`

## How It Works

### Round 1 (Initial Creation)
1. Receives task request with brief and requirements
2. Decodes any attachments (images, data files, etc.)
3. Generates complete web app using GPT-4o
4. Creates new GitHub repository
5. Commits generated files (index.html, README.md, LICENSE)
6. Enables GitHub Pages
7. Notifies evaluation server with repo details and commit SHA

### Round 2 (Improvements)
1. Receives updated task request with new requirements
2. Fetches existing README from the repository
3. Generates improved version based on feedback
4. Updates files in existing repository
5. Re-deploys to GitHub Pages
6. Notifies evaluation server with updated details

## Code Structure

### app.py
- FastAPI application with CORS enabled
- Request validation and secret verification
- Background task processing
- Duplicate request handling

### llm_generator.py
- OpenAI GPT-4o integration
- Attachment decoding and processing
- Code generation with structured output
- README generation with fallback

### github_utils.py
- Repository creation and management
- File commit operations (text and binary)
- GitHub Pages enablement
- MIT license generation

### notify.py
- HTTP POST to evaluation servers
- Retry logic with exponential backoff
- Response validation

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4o | Yes |
| `GITHUB_TOKEN` | GitHub Personal Access Token | Yes |
| `GITHUB_USERNAME` | Your GitHub username | Yes |
| `USER_SECRET` | Secret key for request validation | Yes |

## Error Handling

- Invalid secret → Returns error immediately
- Duplicate requests → Re-notifies with cached response
- LLM failure → Falls back to basic HTML template
- GitHub API errors → Logged and handled gracefully
- Notification failures → Retries with exponential backoff

## Limitations

- Generates single-file HTML applications (inline CSS/JS)
- Limited to public GitHub repositories
- Requires active OpenAI API credits
- Free Hugging Face Spaces may sleep after inactivity

## Contributing

This is an academic project for the Tools in Data Science course.

## License

MIT License - See LICENSE file for details

## Author

Created for TDS Project 1 - LLM Code Deployment

## Acknowledgments

- OpenAI GPT-4o for code generation
- GitHub API for repository management
- FastAPI for the web framework
- Hugging Face for deployment platform