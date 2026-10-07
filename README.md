# Parth Construction - Daily Shorts/Reels Automation

Everything uses the Gmail account **parthconstruction018@gmail.com** (YouTube, Google Cloud, GitHub).

## What is automated and what is not
| Step | How |
|---|---|
| 30-day story/scripts/titles/tags/prompts | Done: `content_plan.csv` (Claude) |
| Video with audio | Gemini (Veo) - you paste `gemini_video_prompt` (about 2 min/day) |
| Thumbnail | ChatGPT - you paste `chatgpt_thumbnail_prompt` |
| Upload + post at 5:55 PM IST daily | Automatic (GitHub Actions + `poster.py`) |

Gemini and ChatGPT have no free public API for video/image generation, so those two steps are manual.
Tip: make 7 videos in one sitting each weekend and commit them to `queue/dayNN/`.

## Gemini logo
Do not use tools to erase the Gemini watermark; that can violate Gemini's terms and risks the channel.
Instead: generate in the Gemini plan that exports without the visible mark, or crop/zoom the frame slightly
in the free CapCut/DaVinci editor, add your own "Parth Construction" logo, and keep AI disclosure on.

## One-time setup (about 45 min)
1. GitHub (sign up with the Gmail above): create a **public** repo, upload this folder.
2. Google Cloud Console: new project, enable **YouTube Data API v3**, create an OAuth **Desktop** client,
   download `client_secret.json`, add the Gmail as a test user. Run `python setup_youtube_auth.py`.
3. Instagram: switch the account to Professional (Creator/Business), link a Facebook Page, create a Meta app
   with Instagram Graph API, and get `IG_USER_ID` and a long-lived `IG_ACCESS_TOKEN`.
4. Repo Settings > Secrets and variables > Actions:
   - Secrets: `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`, `IG_USER_ID`, `IG_ACCESS_TOKEN`
   - Variables: `START_DATE` (e.g. 2026-10-08), `PUBLIC_BASE_URL` (https://raw.githubusercontent.com/<user>/<repo>/main)

## Daily routine
Put `video.mp4` (and `thumb.jpg`) in `queue/dayNN/`. At 5:55 PM IST the workflow posts that day.
Test any time: Actions tab > Run workflow, or `python poster.py 1`.

## Reality check on Rs 50,000/month
YouTube pays only after joining the Partner Programme (1,000 subs + 4,000 public watch hours or
10M Shorts views in 90 days; the lower tier of 500 subs gets fan-funding features only).
Shorts revenue per 1,000 views is small, so Rs 50k from Shorts alone needs a very large audience.
Faster paths: add 1 long video per week, and use the channel to get construction leads, material affiliate links, and
service enquiries, which pay far more than ad revenue.
