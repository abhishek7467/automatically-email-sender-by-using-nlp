from google.oauth2 import service_account
from googleapiclient.discovery import build
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()

def split_text(text):
    splitter = RecursiveCharacterTextSplitter( separators='\n',chunk_size=100, chunk_overlap=10)
    return splitter.split_text(text)

def load_google_doc_text(document_id: str, service_account_file: str):
    """
    Load text from a Google Doc using the Google Docs API.
    """
    # Authenticate with Google
    SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES
    )
    service = build('docs', 'v1', credentials=creds)
    document = service.documents().get(documentId=document_id).execute()
    # Extract plain text
    text = []
    for content in document.get('body', {}).get('content', []):
        if 'paragraph' in content:
            for element in content['paragraph']['elements']:
                if 'textRun' in element:
                    text.append(element['textRun']['content'])
    text_lst_split= split_text(''.join(text))
    return text_lst_split
