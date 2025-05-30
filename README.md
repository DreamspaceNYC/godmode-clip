# GodMode Viral Clip API (Render Deploy)

## How to Use

1. Create a new private GitHub repo and upload this project.
2. Go to [Render](https://dashboard.render.com) > New Web Service.
3. Connect your repo.
4. Set Environment:
   - Runtime: Docker
   - Port: 8080
   - Start Command: uvicorn api:app --host 0.0.0.0 --port 8080
5. Add these ENV VARS:
   - BOT_TOKEN: Your Telegram bot token
   - CHAT_ID: Your target chat ID (e.g. 6681470587)