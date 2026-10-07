"""Posts today's queue/dayNN video to YouTube Shorts and Instagram Reels.

Env vars (GitHub Secrets):
  START_DATE          first posting day, YYYY-MM-DD (IST)
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN   (from setup_youtube_auth.py)
  IG_USER_ID, IG_ACCESS_TOKEN                         (Instagram Graph API)
  PUBLIC_BASE_URL     e.g. https://raw.githubusercontent.com/<user>/<repo>/main
Files per day: queue/dayNN/video.mp4, thumb.jpg (optional), meta.json
"""
import json, os, sys, time, datetime, urllib.parse
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))

def today_folder():
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        start = datetime.date.fromisoformat(os.environ["START_DATE"])
        n = (datetime.datetime.now(IST).date() - start).days + 1
    if not 1 <= n <= 30:
        sys.exit(f"Day {n} is outside the 30-day queue; add new content.")
    return f"queue/day{n:02d}"

def post_youtube(folder, meta):
    creds = Credentials(None, refresh_token=os.environ["YT_REFRESH_TOKEN"],
                        client_id=os.environ["YT_CLIENT_ID"], client_secret=os.environ["YT_CLIENT_SECRET"],
                        token_uri="https://oauth2.googleapis.com/token")
    yt = build("youtube", "v3", credentials=creds)
    body = {"snippet": {"title": meta["title"][:90] + " #Shorts", "description": meta["description"],
                        "tags": meta["tags"], "categoryId": "27"},
            # AI-generated realistic video must be disclosed to YouTube
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False,
                       "containsSyntheticMedia": True}}
    media = MediaFileUpload(f"{folder}/video.mp4", chunksize=-1, resumable=True, mimetype="video/mp4")
    resp = yt.videos().insert(part="snippet,status", body=body, media_body=media).execute()
    vid = resp["id"]
    thumb = f"{folder}/thumb.jpg"
    if os.path.exists(thumb):
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(thumb)).execute()
        except Exception as e:
            print("Thumbnail skipped:", e)
    print("YouTube posted:", f"https://youtube.com/shorts/{vid}")

def post_instagram(folder, meta):
    uid, tok = os.environ["IG_USER_ID"], os.environ["IG_ACCESS_TOKEN"]
    url = f"{os.environ['PUBLIC_BASE_URL']}/{urllib.parse.quote(folder)}/video.mp4"
    g = f"https://graph.instagram.com/v21.0"
    r = requests.post(f"{g}/{uid}/media", data={"media_type": "REELS", "video_url": url,
                      "caption": meta["description"][:2200], "access_token": tok}, timeout=60)
    r.raise_for_status()
    cid = r.json()["id"]
    for _ in range(40):  # wait for processing
        s = requests.get(f"{g}/{cid}", params={"fields": "status_code", "access_token": tok}, timeout=30).json()
        if s.get("status_code") == "FINISHED":
            break
        if s.get("status_code") == "ERROR":
            sys.exit(f"Instagram processing failed: {s}")
        time.sleep(15)
    p = requests.post(f"{g}/{uid}/media_publish", data={"creation_id": cid, "access_token": tok}, timeout=60)
    p.raise_for_status()
    print("Instagram posted:", p.json())

if __name__ == "__main__":
    folder = today_folder()
    if not os.path.exists(f"{folder}/video.mp4"):
        sys.exit(f"No video.mp4 in {folder}. Add the video first.")
    meta = json.load(open(f"{folder}/meta.json", encoding="utf-8"))
    errors = []
    for fn in (post_youtube, post_instagram):
        try:
            fn(folder, meta)
        except Exception as e:
            errors.append(f"{fn.__name__}: {e}")
    if errors:
        sys.exit("\n".join(errors))
