# --- Base image ---
FROM python:3.12-slim

# --- Set working directory ---
WORKDIR /app

# --- Copy project files ---
COPY . /app

# --- Install dependencies ---
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# --- Expose HF Spaces default port ---
EXPOSE 7860

# --- Run FastAPI ---
# app.py is the root file, imports app from app.main
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]


