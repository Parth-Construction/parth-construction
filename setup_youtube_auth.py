"""Run once on your laptop, signed in as parthconstruction018@gmail.com, to get a YouTube refresh token.
Needs client_secret.json (OAuth Desktop app) from Google Cloud Console, YouTube Data API v3 enabled."""
from google_auth_oauthlib.flow import InstalledAppFlow
flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json", ["https://www.googleapis.com/auth/youtube.upload"])
creds = flow.run_local_server(port=0)
print("YT_CLIENT_ID    =", creds.client_id)
print("YT_CLIENT_SECRET=", creds.client_secret)
print("YT_REFRESH_TOKEN=", creds.refresh_token)
