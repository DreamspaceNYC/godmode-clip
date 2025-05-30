from fastapi import FastAPI, Request
import subprocess, os, requests
import yt_dlp
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.post("/clip")
async def clip(request: Request):
    data = await request.json()
    url = data.get("url", "")
    video_id = url.split("?v=")[-1].split("&")[0]
    title = "Untitled"

    # Extract video title
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Your viral clip is ready!')
    except Exception as e:
        print("Title fetch failed:", e)

    raw_path = f"/tmp/{video_id}.mp4"
    final_path = f"/tmp/{video_id}_final.mp4"

    # Step 1: Download 2:30 to 3:00 segment (customizable)
    dl_cmd = f"yt-dlp -f 'bv[height<=720]+ba' --download-sections '*00:02:30-00:03:00' -o '{raw_path}' '{url}'"
    subprocess.run(dl_cmd, shell=True)

    # Step 2: Convert to vertical 1080x1920 + watermark
    ffmpeg_cmd = (
        f"ffmpeg -y -i '{raw_path}' "
        f"-vf \"scale=1080:1920,drawtext=text='GODMODE':x=20:y=20:fontsize=48:fontcolor=white\" "
        f"-c:a copy '{final_path}'"
    )
    subprocess.run(ffmpeg_cmd, shell=True)

    # Step 3: Send to Telegram
    with open(final_path, "rb") as f:
        files = {"video": f}
        data = {
            "chat_id": CHAT_ID,
            "caption": title,
            "supports_streaming": True
        }
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo",
            data=data,
            files=files
        )

    return {"status": "✅ Done", "telegram_response": r.json()}
