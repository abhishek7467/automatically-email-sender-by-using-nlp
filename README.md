# 📧 Email Automation Workflow By Using the Langgraph, Google Gemini, Pinecone vector db

An intelligent email automation system that leverages AI to process emails, generate responses, and manage workflows using Google APIs, Pinecone vector database, and Google Gemini AI.

## 🚀 Features
- **Smart Email Processing**: Automatically read and categorize incoming emails
- **AI-Powered Responses**: Generate contextual email responses using Google Gemini
- **Vector Search**: Store and retrieve email contexts using Pinecone vector database
- **Google Integration**: Seamless integration with Gmail and Google Docs APIs
- **Workflow Automation**: Automated email workflows with LangGraph
- **Secure Authentication**: OAuth 2.0 and service account authentication

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [How to Run](#how-to-run)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

## 🛠️ Prerequisites

Before you begin, ensure you have the following:

- Python 3.8 or higher
- Google Account (personal or Google Workspace)
- Google Cloud Platform account with billing enabled
- Pinecone account
- Git installed on your system

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd email_automation_workflow
```

### 2. Create Virtual Environment

```bash
python -m venv email_automation_env
source email_automation_env/bin/activate  # On Windows: email_automation_env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Credentials

Follow the detailed setup guide in [`info.md`](./info.md) to configure:
- Google Cloud APIs (Gmail, Docs, Drive)
- Pinecone vector database
- Google Gemini API

## ⚙️ Configuration

### 1. Environment Variables

Create a `.env` file in the project root:

```env
# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment_here
PINECONE_INDEX_NAME=automate-email-pinecone 

and PINECONE_INDEX_NAME index settings should be like
Metric -> cosine
Dimensions -> 3072
Type -> Dense
Capacity mode -> Serverless

# Google Docs Configuration
DOC_ID=your_google_doc_id_here # Google Document ID

# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=./google_creds/service_account.json
OAUTH_CLIENT_SECRET=./google_creds/client_secret_xxx.json

# Email Configuration
SENDER_EMAIL=your_email@domain.com
```


### 2. Google Credentials

#### 2.1 Create Google Docs File
Create a Google Docs file with email addresses in the following format:
```
name        | email
abhishek    | abhi123@gmail.com
surender    | surender@gmail.com
abhishek kumar   | abhishek123@gmail.com
```

#### 2.2 Set Up Google Cloud Credentials
Place your credential files in the `google_creds/` directory:
- `service_account.json` - Service account credentials
- `client_secret_xxx.json` - OAuth client credentials
- `token.json` - OAuth token (generated automatically)

#### 2.3 Generate Token File
Run the token generation script:
```bash
python token_generate.py
```

### 3. Verify Installation
Run the verification scripts mentioned in [`info.md`](./info.md) to ensure all services are properly configured.

## 🎯 How to Run

### Method 1: Run the Main Script
```bash
python main.py
```

### Method 2: Run with Options
```bash
# Test mode without sending emails
python main.py --dry-run

# Process only specific number of emails
python main.py --limit 10

# Process emails from specific sender
python main.py --sender specific@email.com

# Show help
python main.py --help
```

### Method 3: Step-by-Step Process

1. **First, generate authentication token:**
   ```bash
   python token_generate.py
   ```

2. **Run the email automation workflow:**
   ```bash
   python main.py
   ```

3. **Monitor the process:**
   - Check console output for processing status
   - Review log files for detailed information
   - Verify sent emails in your Gmail account

## � Usage

### Basic Email Automation

Once the system is configured and running, it will automatically:

1. **Monitor Your Gmail**: Continuously checks for new, unread emails
2. **Analyze Content**: Uses AI to understand the context and intent of each email
3. **Generate Responses**: Creates appropriate replies using Google Gemini AI
4. **Send Replies**: Automatically sends contextual responses to the email senders

### Working with Different Email Types

The system can handle various types of emails:

- **Business Inquiries**: Professional responses for business-related emails
- **Support Requests**: Helpful responses for customer support queries
- **General Questions**: Informative replies for general inquiries
- **Follow-ups**: Contextual responses based on previous conversations

### Customizing Responses

You can customize the AI responses by:

1. **Modifying Prompts**: Edit the AI prompts in `modules/ai_utils.py`
2. **Adding Context**: Update the Google Docs file with relevant information
3. **Training Vector DB**: Add more email examples to improve context matching

### Managing Email Processing

#### Manual Control Options:
```bash

# Chat mode with query
python main.py --option chat --query "send a email to abhishek kumar for asking about the leave for tommorow sept 16 due to some urgent work."

# Data store mode
python main.py --option data_store

```

#### Monitoring and Logs:
- **Console Output**: Real-time processing status
- **Email Confirmations**: Check your Gmail sent folder
- **Error Handling**: System logs errors and continues processing

### Best Practices

1. **Start with Test Mode**: Always run `--dry-run` first to test configurations
2. **Monitor Responses**: Regularly check the generated responses for quality
3. **Update Context**: Keep your Google Docs file updated with current information
4. **Backup Tokens**: Save your authentication tokens securely
5. **Regular Maintenance**: Periodically refresh tokens and update credentials

### Integration Workflow

```
📧 New Email Arrives
    ↓
🔍 AI Analyzes Content
    ↓
🔎 Search Vector Database for Similar Conversations
    ↓
🤖 Generate Contextual Response using Gemini AI
    ↓
📤 Send Automated Reply
    ↓
💾 Store Conversation for Future Reference
```

### Advanced Usage

For more advanced use cases:

1. **Custom Email Filters**: Modify `modules/utils.py` to add custom filtering logic
2. **Response Templates**: Create template responses for common scenarios
3. **Scheduling**: Set up cron jobs to run the automation at specific intervals
4. **Integration**: Connect with other systems via the API modules

## �📊 What the System Does

1. **Reads Incoming Emails**: Connects to Gmail and fetches unread emails
2. **Processes Content**: Uses AI to analyze email content and context
3. **Searches Vector Database**: Finds similar past conversations using Pinecone
4. **Generates Responses**: Creates appropriate replies using Google Gemini AI
5. **Sends Automated Replies**: Sends contextual responses back to senders
6. **Updates Records**: Stores conversation history for future reference

## 📁 Project Structure

```
email_automation_workflow/
├── google_creds/                 # Google API credentials
│   ├── service_account.json
│   ├── client_secret_xxx.json
│   └── token.json
├── modules/                      # Core modules
│   ├── ai_utils.py              # AI/Gemini integration
│   ├── create_update_index.py   # Pinecone vector operations
│   ├── langgraph_work.py        # Workflow automation
│   ├── pydantic_obj.py          # Data models
│   ├── send_mail.py             # Email sending functionality
│   └── utils.py                 # Utility functions
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
├── info.md                      # Setup guide
├── README.md                    # This file
├── main.py                      # Main entry point
└── token_generate.py            # Token generation script
```

## 🔧 Core Components

- **`main.py`**: Main entry point for the email automation system
- **`token_generate.py`**: Generates OAuth tokens for Google API access
- **`modules/langgraph_work.py`**: Orchestrates the entire email workflow
- **`modules/ai_utils.py`**: Handles AI responses using Google Gemini
- **`modules/send_mail.py`**: Manages email sending functionality
- **`modules/utils.py`**: Utility functions for email processing
- **`modules/create_update_index.py`**: Manages Pinecone vector database operations

## 🔍 Troubleshooting

### Common Issues

1. **Authentication Errors**
   ```
   Error: 403 Forbidden
   Solution: Check API enablement and credentials in info.md
   ```

2. **Pinecone Connection Issues**
   ```
   Error: Unable to connect to Pinecone
   Solution: Verify API key and environment in .env file
   ```

3. **Email Sending Failures**
   ```
   Error: Unable to send email
   Solution: Check OAuth scopes and domain delegation
   ```

4. **Token Errors**
   ```
   Error: Token expired or invalid
   Solution: Run python token_generate.py to refresh tokens
   ```

### Debug Tips

1. **Check Environment Variables**: Ensure all required variables are set in `.env` file
2. **Verify Credentials**: Make sure all credential files are in the correct location
3. **Test API Access**: Use the verification scripts in `info.md`
4. **Check Permissions**: Ensure your Google account has necessary permissions

### Getting Help

If you encounter issues:
1. Check the [info.md](./info.md) file for detailed setup instructions
2. Verify all prerequisites are met
3. Ensure all credential files are properly configured
4. Run the token generation script if authentication fails

---

**📧 Happy Emailing!** 🚀

For detailed setup instructions and API configurations, please refer to [`info.md`](./info.md).
