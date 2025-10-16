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

# --- Set environment variables ---
# Make sure your env.txt is copied or set secrets via Hugging Face UI
ENV USER_SECRET=replace_with_secret
ENV GITHUB_TOKEN=replace_with_token
ENV GITHUB_USERNAME=replace_with_username
ENV OPENAI_API_KEY=replace_with_key

# --- Run FastAPI via Uvicorn ---
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
