# Email Automation Workflow Setup Guide

This guide provides a complete, step-by-step setup process for configuring Google Cloud (Docs + Gmail), Pinecone, and Gemini API to enable automated email workflow functionality.

## 📋 Prerequisites

- Google Account (personal or Google Workspace)
- Valid billing account for Google Cloud (free tier available)
- Internet connection and web browser

## 🔗 Important URLs

- **Google Cloud Console**: https://console.cloud.google.com/
- **Google Admin Console**: https://admin.google.com (for Google Workspace users)
- **Pinecone Console**: https://app.pinecone.io/
- **Gemini AI Studio**: https://aistudio.google.com/app/apikey

---

## 🟢 Part 1: Google Cloud Setup (Docs + Gmail API)

### Step 1: Create Google Cloud Project

1. Navigate to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the **Project Dropdown** (next to "Google Cloud" logo)
3. Click **"New Project"**
4. Enter project details:
   - **Project Name**: `gmail-automation-project` (or your preferred name)
   - **Organization**: Select your organization (if applicable)
   - **Location**: Choose appropriate location
5. Click **"Create"**
6. Wait for project creation (may take a few minutes)
7. Ensure the new project is selected in the project dropdown

### Step 2: Enable Required APIs

1. Go to **APIs & Services** → **Library**
2. Search and enable the following APIs (one by one):

#### Enable Google Docs API:
   - Search for "**google docs API**"
   - Click on "**Google Docs API**"
   - Click **"Enable"**
   - Wait for confirmation

#### Enable Gmail API:
   - Search for "**gmail API**"
   - Click on "**Gmail API**"
   - Click **"Enable"**
   - Wait for confirmation

#### Enable Google Drive API (Optional but Recommended):
   - Search for "**google drive API**"
   - Click on "**Google Drive API**"
   - Click **"Enable"**
   - Wait for confirmation

### Step 3: Create Service Account

1. Go to **APIs & Services** → **Credentials**
2. Click **"+ Create Credentials"** → **"Service Account"**
3. Fill in service account details:
   - **Service account name**: `gmail-automation-sa`
   - **Service account ID**: Will auto-populate
   - **Description**: `Service account for email automation workflow`
4. Click **"Create and Continue"**
5. Grant service account access:
   - **Role**: Select **"Editor"** or **"Owner"** for full access
   - Click **"Continue"**
6. Grant users access (optional):
   - Leave blank for now
   - Click **"Done"**

### Step 4: Create and Download JSON Key

1. Go back to **APIs & Services** → **Credentials**
2. Find your newly created Service Account in the list
3. Click on the service account name
4. Go to the **"Keys"** tab
5. Click **"Add Key"** → **"Create New Key"**
6. Select **"JSON"** format
7. Click **"Create"**
8. The JSON file will automatically download (e.g., `gen-lang-client-0288089509-3b9278a23b50.json`)

**⚠️ Important**: 
- Save this JSON file securely
- Rename it to something recognizable like `service_account.json`
- Place it in your project's `google_creds/` directory

### Step 5: Domain-Wide Authority (For Google Workspace)

**Note**: This step is only required if you're using a Google Workspace account (company/organization email).

1. Navigate to [Google Admin Console](https://admin.google.com)
2. Go to **Security** → **API Controls** → **Domain-wide Delegation**
3. Click **"Add New"**
4. Configure delegation:
   - **Client ID**: Copy from your service account JSON file (client_id field)
   - **OAuth Scopes**: Add the following scopes (comma-separated):
     ```
     https://www.googleapis.com/auth/gmail.send,
     https://www.googleapis.com/auth/gmail.readonly,
     https://www.googleapis.com/auth/userinfo.email,
     https://www.googleapis.com/auth/documents,
     https://www.googleapis.com/auth/drive
     ```
5. Click **"Authorize"**

### Step 6: OAuth Setup (For Personal Gmail Accounts)

**Note**: Personal Gmail accounts cannot use service accounts for sending emails. Use OAuth 2.0 instead.

1. Go to **APIs & Services** → **Credentials**
2. Click **"+ Create Credentials"** → **"OAuth Client ID"**
3. If prompted, configure OAuth consent screen:
   - **User Type**: External
   - Fill in required fields (App name, User support email, etc.)
   - Add your email to test users
4. Create OAuth Client ID:
   - **Application Type**: Desktop Application
   - **Name**: `Gmail Automation Client`
5. Click **"Create"**
6. Download the JSON file (e.g., `client_secret_xxx.json`)
7. Place this file in your `google_creds/` directory

---

## 🟡 Part 2: Pinecone Vector Database Setup

### Step 1: Create Pinecone Account

1. Navigate to [Pinecone Console](https://app.pinecone.io/)
2. Click **"Sign Up"** or **"Get Started Free"**
3. Create account with email or Google sign-in
4. Verify your email address
5. Complete the onboarding process

### Step 2: Get API Key and Environment

1. In the Pinecone dashboard, go to **"API Keys"** in the sidebar
2. Copy the following information:
   - **API Key**: Your unique API key
   - **Environment**: Your region (e.g., `us-east1-gcp`, `us-west4-gcp`)

### Step 3: Create Vector Index

1. Go to **"Indexes"** in the sidebar
2. Click **"Create Index"**
3. Configure your index:
   - **Index Name**: `automate-email-pinecone`
   - **Dimension**: `1536` (for OpenAI Ada-002 embeddings) or `768` (for sentence transformers)
   - **Metric**: `cosine`
   - **Pod Type**: `p1.x1` (starter pod)
4. Click **"Create Index"**
5. Wait for index creation (may take a few minutes)

### Step 4: Environment Configuration

Create a `.env` file in your project root with:
```env
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment_here
PINECONE_INDEX_NAME=automate-email-pinecone
```

---

## 🔵 Part 3: Google Gemini API Setup

### Step 1: Get Gemini API Key

1. Navigate to [Gemini AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Select your Google Cloud project (the one created in Part 1)
5. Click **"Create API Key in New Project"** or use existing project
6. Copy the generated API key

### Step 2: Environment Configuration

Add to your `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 3: Install Required Python Packages

Run the following commands in your terminal:
```bash
pip install google-generativeai
pip install google-auth google-auth-oauthlib google-auth-httplib2
pip install google-api-python-client
pip install pinecone-client
```

---

## 🛠️ Part 4: Project Configuration

### Directory Structure

Ensure your project has the following structure:
```
email_automation_workflow/
├── google_creds/
│   ├── service_account.json              # Service account key
│   ├── client_secret_xxx.json           # OAuth client secret (for personal Gmail)
│   └── token.json                       # OAuth token (generated automatically)
├── modules/
│   ├── ai_utils.py
│   ├── send_mail.py
│   └── ...other modules
├── .env                                 # Environment variables
├── requirements.txt
└── main.py
```

### Environment Variables File (.env)

Create a complete `.env` file:
```env
# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment_here
PINECONE_INDEX_NAME=automate-email-pinecone

# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=./google_creds/service_account.json
OAUTH_CLIENT_SECRET=./google_creds/client_secret_xxx.json

# Email Configuration
SENDER_EMAIL=your_email@domain.com
```

### Requirements.txt

Ensure your `requirements.txt` includes:
```txt
google-generativeai>=0.3.0
google-auth>=2.17.0
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.1.0
google-api-python-client>=2.88.0
pinecone-client>=2.2.0
python-dotenv>=1.0.0
pydantic>=2.0.0
langchain>=0.1.0
langgraph>=0.0.1
email-validator>=2.0.0
```

---

## ✅ Verification Steps

### Test Google Cloud Setup

```python
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Test Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def test_gmail_connection():
    creds = None
    if os.path.exists('google_creds/token.json'):
        creds = Credentials.from_authorized_user_file('google_creds/token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google_creds/client_secret_xxx.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('google_creds/token.json', 'w') as token:
            token.write(creds.to_json())
    
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().labels().list(userId='me').execute()
    print("Gmail connection successful!")
    return True

test_gmail_connection()
```

### Test Pinecone Setup

```python
import pinecone
import os
from dotenv import load_dotenv

load_dotenv()

def test_pinecone_connection():
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),
        environment=os.getenv("PINECONE_ENVIRONMENT")
    )
    
    index_name = os.getenv("PINECONE_INDEX_NAME")
    if index_name in pinecone.list_indexes():
        index = pinecone.Index(index_name)
        stats = index.describe_index_stats()
        print(f"Pinecone connection successful! Index stats: {stats}")
        return True
    else:
        print(f"Index {index_name} not found!")
        return False

test_pinecone_connection()
```

### Test Gemini API Setup

```python
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def test_gemini_connection():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Hello Gemini! This is a test.")
    print(f"Gemini connection successful! Response: {response.text}")
    return True

test_gemini_connection()
```

---

## 🚨 Troubleshooting

### Common Issues and Solutions

1. **"403 Forbidden" Error**:
   - Ensure APIs are enabled in Google Cloud Console
   - Check service account permissions
   - Verify domain-wide delegation (for Google Workspace)

2. **"Invalid Credentials" Error**:
   - Verify JSON file path and permissions
   - Ensure OAuth scopes are correct
   - Regenerate credentials if necessary

3. **Pinecone Connection Error**:
   - Verify API key and environment
   - Check index name spelling
   - Ensure sufficient Pinecone quota

4. **Gemini API Error**:
   - Verify API key is correct
   - Check API quota and billing
   - Ensure proper model name

### Support Resources

- **Google Cloud Documentation**: https://cloud.google.com/docs
- **Pinecone Documentation**: https://docs.pinecone.io
- **Gemini API Documentation**: https://ai.google.dev/docs

---

## 📝 Final Checklist

- [ ] Google Cloud project created
- [ ] Google Docs API enabled
- [ ] Gmail API enabled
- [ ] Service account created and JSON downloaded
- [ ] Domain-wide delegation configured (if using Google Workspace)
- [ ] OAuth client created (if using personal Gmail)
- [ ] Pinecone account created
- [ ] Pinecone API key obtained
- [ ] Pinecone index created
- [ ] Gemini API key obtained
- [ ] Environment variables configured
- [ ] Required packages installed
- [ ] Connection tests passed

Once all items are checked, your email automation workflow should be ready to use!

---

**⚠️ Security Note**: Never commit credential files (`.json`, `.env`) to version control. Add them to your `.gitignore` file to keep your credentials secure.