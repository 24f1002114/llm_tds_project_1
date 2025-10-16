FROM python:3.12-slim
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

# Use Secrets instead of hardcoding sensitive info
# ENV USER_SECRET=replace_with_secret
# ENV GITHUB_TOKEN=replace_with_token
# ENV OPENAI_API_KEY=replace_with_key

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
