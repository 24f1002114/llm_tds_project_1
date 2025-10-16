FROM python:3.12-slim
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

# Use your app.py as entry point
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
