# 🧠 AI-Powered GitHub Automation with Gemini + FastAPI

An automated system that takes plain text prompts, generates production-grade code using **Google Gemini**, commits the results directly to **GitHub**, and even deploys **GitHub Pages** — all through a single FastAPI endpoint.

---

## 🚀 Features

- **LLM-Driven Code Generation:**  
  Automatically builds complete codebases from plain language requests.

- **FastAPI Orchestration:**  
  Handles incoming requests, background processing, and response delivery.

- **GitHub Integration:**  
  Creates repositories, commits generated files, and enables GitHub Pages hosting.

- **Persistent Task Management:**  
  Prevents duplicate requests via local tracking of processed inputs.

- **Asynchronous Background Execution:**  
  Keeps API responsive while handling long-running code generation.

---

## 🧩 Tech Stack

| Component | Purpose |
|------------|----------|
| **FastAPI** | Core web framework & background task runner |
| **Google Gemini API** | AI code generation engine |
| **PyGithub** | GitHub API client for repo management |
| **Python-dotenv** | Secure environment variable management |
| **Uvicorn** | ASGI server for deployment |

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
