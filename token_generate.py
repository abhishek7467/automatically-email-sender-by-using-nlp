from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
from dotenv import load_dotenv
import pickle
load_dotenv()
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/userinfo.email"
]

GOOGLE_EMAIL_TOKEN = os.getenv("GOOGLE_EMAIL_TOKEN")
GOOGLE_EMAIL_CREDENTIALS = os.getenv("GOOGLE_EMAIL_CREDENTIALS")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")


def get_gmail_service():
    """Authenticate user via OAuth2 and return Gmail service."""
    creds = None
    if os.path.exists(GOOGLE_EMAIL_TOKEN):
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file(GOOGLE_EMAIL_TOKEN, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
                # "google_creds/email_send_client_secret_417557973889-9ts8k5ss5018i85lko8t3c3j9f24th4a.apps.googleusercontent.com.json",
            flow = InstalledAppFlow.from_client_secrets_file(
                GOOGLE_EMAIL_CREDENTIALS,
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

        # save credentials for reuse
        with open(GOOGLE_EMAIL_TOKEN, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)
import traceback
# --- Test ---
service = get_gmail_service()
profile = service.users().getProfile(userId="me").execute()
print("📧 Logged in as:", profile.get("emailAddress"))