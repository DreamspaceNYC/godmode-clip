FROM python:3.11-slim

RUN apt update && apt install -y ffmpeg curl && \
    pip install fastapi uvicorn yt-dlp python-dotenv requests

WORKDIR /app
COPY . /app

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]