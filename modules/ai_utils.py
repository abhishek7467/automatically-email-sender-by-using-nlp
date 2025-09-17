from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone
from modules.send_mail import mail_node
import os
from dotenv import load_dotenv
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage
load_dotenv()
# ---- CONFIG ----
pc = Pinecone()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("SERVICE_ACCOUNT_FILE")
# ---- EMBEDDING MODEL ----
embed_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001",google_api_key=os.getenv("GOOGLE_API_KEY"))

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# 1️⃣ Define structured schema
class EmailResponse(BaseModel):
    to: List[str] = Field(description="List of recipient email addresses to send the email to")
    cc: Optional[List[str]] = Field(default=[], description="List of CC email addresses (if any)")
    subject: str = Field(description="Subject line of the email")
    body: str = Field(description="Body of the email as plain text")
    reason: str = Field(description="Why these recipients were chosen, based on context")


# 2️⃣ Define parser
email_parser = PydanticOutputParser(pydantic_object=EmailResponse)

# 3️⃣ Create prompt template with format instructions
email_prompt_template = PromptTemplate(
    template="""
You are an AI email assistant. Your job is to draft a professional email based on the user query
and the provided context. Extract recipients from the context if possible.

Context:
{context}

User Query:
{query}

Generate a JSON output with the following fields:
{format_instructions}

return always proper html body for formatting. 
Best regards,\n Abhishek Kumar\n

""",
    input_variables=["context", "query"],
    partial_variables={"format_instructions": email_parser.get_format_instructions()},
)

def chat_node(state: "GmailAutomateState") -> Dict:
    """
    Chat node: performs RAG query on Pinecone, then generates structured email response.
    """

    query = getattr(state, "query", None)
    if not query:
        return {"response": "No query provided."}

    # ✅ Recreate Pinecone index on the fly (do NOT store in state)
    try:
        index = pc.Index(state.index_name)
    except Exception as e:
        return {"response": f"Error loading Pinecone index: {e}"}

    # 1️⃣ Embed the query
    query_embedding = embed_model.embed_query(query)

    # 2️⃣ Search Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=3,
        namespace=state.nameSpaces,
        include_metadata=True
    )

    # 3️⃣ Collect retrieved text
    retrieved_texts = [
        match["metadata"]["text"]
        for match in results.get("matches", [])
        if "metadata" in match and "text" in match["metadata"]
    ]

    if not retrieved_texts:
        return {"response": "No relevant information found in the knowledge base."}

    context = "\n".join(retrieved_texts)

    # 4️⃣ Build prompt
    prompt = email_prompt_template.format(context=context, query=query)

    # 5️⃣ Invoke LLM
    raw_answer = llm.invoke(prompt)

    # 6️⃣ Extract text
    if isinstance(raw_answer, AIMessage):
        raw_text = raw_answer.content
    elif isinstance(raw_answer, str):
        raw_text = raw_answer
    else:
        raw_text = str(raw_answer)


    # 7️⃣ Parse structured output
    try:
        parsed_output = email_parser.parse(raw_text)
    except Exception as e:
        return {"response": f"Failed to parse LLM output: {e}", "raw_output": raw_text}
    parsed_output=parsed_output.model_dump()
    
    state.email_to = parsed_output.get("to", [])
    state.email_cc = parsed_output.get("cc", [])
    state.email_subject = parsed_output.get("subject", "")
    state.email_body = parsed_output.get("body", "")

    res = mail_node(state)
    
    return {
        "response": parsed_output,
        "retrieved_docs": retrieved_texts
    }
