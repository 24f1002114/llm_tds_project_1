# app.py at root
# Imports FastAPI instance from your folder
from app.main import app

# Optional: add startup events or logging if needed
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
