import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/userinfo.email",
]

GOOGLE_EMAIL_TOKEN = os.getenv("GOOGLE_EMAIL_TOKEN")
GOOGLE_EMAIL_CREDENTIALS = os.getenv("GOOGLE_EMAIL_CREDENTIALS")
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
def mail_node(dictOutput) -> dict:
    # parsed_output = state.model_dump()
    to_list = dictOutput.get("email_to", [])
    cc_list = dictOutput.get("email_cc", [])
    subject = dictOutput.get("email_subject", "No Subject")
    body = dictOutput.get("email_body", "")

    if not to_list:
        return {"status": "error", "message": "No recipients found for email."}

    try:
        service = get_gmail_service()
        profile = service.users().getProfile(userId="me").execute()
        sender_email = profile.get("emailAddress")

        # ✅ Build email properly
        message = MIMEText(body, "html")
        message["to"] = ", ".join(to_list)
        if cc_list:
            message["cc"] = ", ".join(cc_list)
        message["subject"] = subject
        message["from"] = sender_email  # <-- Always use logged-in account

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        send_result = service.users().messages().send(
            userId="me", body={"raw": raw_message}
        ).execute()

        state.sent_email_status = "success"
        state.message_id = send_result.get("id")

        print(f"✅ Email sent successfully to {to_list}")
        return {
            "status": "success",
            "from": sender_email,
            "to": to_list,
            "subject": subject,
            "message_id": send_result.get("id"),
        }

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        print(traceback.print_exc())
        state.sent_email_status = "error"
        return {"status": "error", "message": str(e)}
import traceback