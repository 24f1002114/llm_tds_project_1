from fastapi import FastAPI, Request, BackgroundTasks
import os, json, base64
from dotenv import load_dotenv
from app.llm_generator import generate_app_code, decode_attachments
from app.github_utils import (
    create_repo,
    create_or_update_file,
    enable_pages,
    generate_mit_license,
    create_or_update_binary_file,
)
from app.notify import notify_evaluation_server
import gradio as gr

load_dotenv()
USER_SECRET = os.getenv("USER_SECRET")
USERNAME = os.getenv("GITHUB_USERNAME")
PROCESSED_PATH = "/tmp/processed_requests.json"

# --- FastAPI app ---
app = FastAPI(title="TDS Project API")

# === Persistence helpers ===
def load_processed():
    if os.path.exists(PROCESSED_PATH):
        try:
            return json.load(open(PROCESSED_PATH))
        except json.JSONDecodeError:
            return {}
    return {}

def save_processed(data):
    json.dump(data, open(PROCESSED_PATH, "w"), indent=2)

# === Background processing task ===
def process_request(data):
    round_num = data.get("round", 1)
    task_id = data["task"]
    print(f"⚙ Processing task {task_id}, round {round_num}")

    attachments = data.get("attachments", [])
    saved_attachments = decode_attachments(attachments)

    repo = create_repo(task_id, description=f"Auto-generated app for task: {data['brief']}")

    prev_readme = None
    if round_num == 2:
        try:
            readme = repo.get_contents("README.md")
            prev_readme = readme.decoded_content.decode("utf-8", errors="ignore")
        except Exception:
            prev_readme = None

    gen = generate_app_code(
        data["brief"],
        attachments=attachments,
        checks=data.get("checks", []),
        round_num=round_num,
        prev_readme=prev_readme
    )

    files = gen.get("files", {})
    saved_info = gen.get("attachments", [])

    # Commit attachments
    for att in saved_info:
        path = att["name"]
        try:
            with open(att["path"], "rb") as f:
                content_bytes = f.read()
            if att["mime"].startswith("text") or att["name"].endswith((".md", ".csv", ".json", ".txt")):
                text = content_bytes.decode("utf-8", errors="ignore")
                create_or_update_file(repo, path, text, f"Add attachment {path}")
            else:
                create_or_update_binary_file(repo, path, content_bytes, f"Add binary {path}")
                b64 = base64.b64encode(content_bytes).decode("utf-8")
                create_or_update_file(repo, f"attachments/{att['name']}.b64", b64, f"Backup {att['name']}.b64")
        except Exception as e:
            print("⚠ Attachment commit failed:", e)

    # Commit generated files
    for fname, content in files.items():
        create_or_update_file(repo, fname, content, f"Add/Update {fname}")

    # Commit MIT license
    mit_text = generate_mit_license()
    create_or_update_file(repo, "LICENSE", mit_text, "Add MIT license")

    # Enable GitHub Pages
    pages_ok = enable_pages(task_id) if round_num == 1 else True
    pages_url = f"https://{USERNAME}.github.io/{task_id}/" if pages_ok else None

    try:
        commit_sha = repo.get_commits()[0].sha
    except Exception:
        commit_sha = None

    payload = {
        "email": data["email"],
        "task": data["task"],
        "round": round_num,
        "nonce": data["nonce"],
        "repo_url": repo.html_url,
        "commit_sha": commit_sha,
        "pages_url": pages_url,
    }

    notify_evaluation_server(data["evaluation_url"], payload)

    processed = load_processed()
    key = f"{data['email']}::{data['task']}::round{round_num}::nonce{data['nonce']}"
    processed[key] = payload
    save_processed(processed)

    print(f"✅ Finished task {task_id}, round {round_num}")

# === API endpoints ===
@app.get("/")
def root():
    return {"status": "ok", "note": "API running"}

@app.post("/api-endpoint")
async def receive_request(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()

    if data.get("secret") != USER_SECRET:
        return {"error": "Invalid secret"}

    processed = load_processed()
    key = f"{data['email']}::{data['task']}::round{data['round']}::nonce{data['nonce']}"

    if key in processed:
        prev = processed[key]
        notify_evaluation_server(data.get("evaluation_url"), prev)
        return {"status": "ok", "note": "duplicate handled & re-notified"}

    background_tasks.add_task(process_request, data)
    return {"status": "accepted", "note": f"processing round {data['round']} started"}

# === Gradio interface ===
def gradio_echo(text):
    return f"You typed: {text}"

iface = gr.Interface(fn=gradio_echo, inputs="text", outputs="text")

# Mount Gradio at /gradio
gr.mount_gradio_app(app, iface, path="/gradio")
