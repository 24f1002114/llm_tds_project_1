# --- Base image ---
FROM python:3.12-slim

# --- Set working directory ---
WORKDIR /app

# --- Copy project files ---
COPY . /app

# --- Install dependencies ---
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# --- Expose FastAPI port ---
EXPOSE 8000

# --- Run FastAPI ---
# Module path: app.app → folder 'app', file 'app.py'
# Variable name: app → FastAPI instance
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
