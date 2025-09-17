from langgraph.graph import StateGraph
from modules.pydantic_obj import GmailAutomateState
from modules.create_update_index import select_or_create_index,manage_index_data,embed_and_upsert
from modules.ai_utils import chat_node
from modules.utils import load_google_doc_text
from dotenv import load_dotenv
import os
load_dotenv()

def google_doc_loader_node(state: GmailAutomateState):
    state.doc_text = load_google_doc_text(os.getenv("DOC_ID"), os.getenv("SERVICE_ACCOUNT_FILE"))
    return state

def route_by_option(state: GmailAutomateState):
    if state.option == "data_store":
        return {"__next__": "data_store"}
    return {"__next__": "chat"}


from langgraph.graph import StateGraph, END
def main_graph():
    graph = StateGraph(GmailAutomateState)
    graph.add_node("router", route_by_option)
    graph.add_node("load_doc", google_doc_loader_node)
    graph.add_node("select_index", select_or_create_index)
    graph.add_node("manage_data", manage_index_data)
    graph.add_node("upsert_data", embed_and_upsert)
    graph.add_node("chat_func_index", chat_node)
    graph.set_entry_point("router")

    # ✅ Use add_conditional_edges instead of condition= on add_edge
    graph.add_conditional_edges(
        "router",  # the node to branch from
        lambda state: state.option,  # a function returning branch key
        {
            "chat": "chat_func_index",          # if option == "chat", go to chat node
            "data_store": "load_doc" # if option == "data_store", go to load_doc node
        }
    )

    # Chat Flow
    graph.add_edge("chat_func_index", END)

    # Data Store Flow
    graph.add_edge("load_doc", "select_index")
    graph.add_edge("select_index", "manage_data")
    graph.add_edge("manage_data", "upsert_data")
    graph.add_edge("upsert_data", END)
    app = graph.compile()
    return app
    # result = app.invoke({"option": "chat", "query": "send a email to surender orange for asking about the progress over the ai-hrms system project srtictly with detailed message and in the last also ask for the deployed project link testing?"})
    # print(result)

    # result = app.invoke({"option": "data_store","query":""})