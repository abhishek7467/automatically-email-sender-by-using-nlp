from pydantic import BaseModel,Field
from typing import List, Optional, Any, Dict


class GmailAutomateState(BaseModel):
    option: str 
    doc_text: Optional[List[str]] = None
    index_name: str = "email-automation"
    index: Optional[Any] = None
    nameSpaces: str = "automate-email-pinecone"
    new_index_auto_filled:bool = False
    query:str
    email_parsed_output: Optional[Dict[str, Any]] = {} 
    email_retrieved_docs: Optional[List[dict]] = []  
    retrieved_texts: Optional[List[str]] = []
    sent_email_status: Optional[str] = None
    message_id: Optional[str] = None
    email_to: Optional[List[str]] = Field(default_factory=list)
    email_cc: Optional[List[str]] = Field(default_factory=list)
    email_subject: Optional[str] = None
    email_body: Optional[str] = None




# class EmailState(BaseModel):
#     email_to: List[str] = []
#     email_cc: List[str] = []
#     email_subject: str = ""
#     email_body: str = ""
#     sent_email_status: Optional[str] = None
#     message_id: Optional[str] = None