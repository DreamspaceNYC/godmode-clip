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

    # Extract title
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Your viral clip is ready!')
    except:
        pass

    raw_path = f"/tmp/{video_id}.mp4"
    final_path = f"/tmp/{video_id}_final.mp4"

    # Download viral moment range (2:30–3:00 as default)
    dl_cmd = f"yt-dlp -f 'bv[height<=720]+ba' --download-sections '*00:02:30-00:03:00' -o '{raw_path}' '{url}'"
    subprocess.run(dl_cmd, shell=True)

    # Watermark + vertical format
    ffmpeg_cmd = f"ffmpeg -y -i {raw_path} -vf "scale=1080:1920,drawtext=text='GODMODE':x=20:y=20:fontsize=48:fontcolor=white" -c:a copy {final_path}"
    subprocess.run(ffmpeg_cmd, shell=True)

    # Send to Telegram
    with open(final_path, "rb") as f:
        files = {"video": f}
        data = {"chat_id": CHAT_ID, "caption": title, "supports_streaming": True}
        r = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo", data=data, files=files)

    return {"status": "✅ Done", "telegram_response": r.json()}