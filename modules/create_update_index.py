from modules.langgraph_work import GmailAutomateState
from pinecone import Pinecone
from modules.ai_utils import embed_model
import os
from dotenv import load_dotenv
load_dotenv()
pc = Pinecone()
def select_or_create_index1(state: GmailAutomateState):
    indexes = pc.list_indexes()
    existing_index_names = [idx['name'] for idx in indexes]

    print("Available indexes:")
    for i, idx in enumerate(indexes, start=1):
        print(f"{i}. {idx['name']}")

    while True:
        user_input = input("Enter index number, index name, or type NEW to create a new one: ").strip()

        # ✅ Directly selecting an existing index by name
        if user_input in existing_index_names:
            print(f"✅ Selected existing index: {user_input}")
            state.index_name = user_input
            break

        # ✅ Create or select new index
        elif user_input.lower() == "new":
            new_index_name = input("Enter new index name: ").strip()
            if new_index_name in existing_index_names:
                print(f"ℹ️ Index '{new_index_name}' already exists. Selecting it instead of creating a new one.")
                state.index_name = new_index_name
            else:
                # from pinecone.models import PodSpec
                # pc.create_index(
                #     name=new_index_name,
                #     dimension=3072,
                #     metric="cosine",
                #     spec = PodSpec(
                #                     pod_type="p1",                
                #                     environment="us-east1-aws"   
                #                 )
                #                 )
                from pinecone.models import ServerlessSpec
                pc.create_index(
                    name=new_index_name,
                    dimension=3072,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",          # or "gcp"
                        region="us-east-1"    # check your Pinecone console for available regions
                    )
                )


                print(f"✅ Created new index: {new_index_name}")
                state.index_name = new_index_name
            break

        # ✅ Selecting by number
        elif user_input.isdigit() and 1 <= int(user_input) <= len(indexes):
            selected_index = existing_index_names[int(user_input) - 1]
            print(f"✅ Selected index: {selected_index}")
            state.index_name = selected_index
            break

        else:
            print("❌ Invalid input. Please type a valid index number, existing index name, or 'NEW'.")


    if state.nameSpaces: nameSpace=state.nameSpaces 
    else:  nameSpace='automate-email-pinecone'
    # ✅ Namespace input with default fallback
    ns_input = input(f"Enter namespace to use (default: {nameSpace}): ")
    state.nameSpaces = ns_input.strip() if ns_input.strip() else nameSpace
    return state

def manage_index_data(state: GmailAutomateState):
    index = pc.Index(state.index_name)
    if getattr(state, "new_index_auto_filled", False):
        print("🎉 Setup complete! Document data is already stored in your new index.")
        print("👉 You can now test auto email generation and sending.")
        print("ℹ️ If you want to append or erase data later, please re-run and select this index again.")
        return state

    action = input("Do you want to (E)rase existing data or (A)ppend new data? [E/A]: ").strip().lower()
    if action == "e":
        try:
            print(f"🧹 Clearing index in namespace: '{state.nameSpaces}'")
            index.delete(delete_all=True, namespace=state.nameSpaces)
            print("✅ Index cleared successfully!")
        except Exception as e:
            if "Namespace not found" in str(e):
                print(f"⚠️ Namespace '{state.nameSpaces}' not found. Nothing to delete.")
            else:
                raise
    elif action == "a":
        user_input = input(
            "Do you want to append new data?\n"
            "Please provide data in the format:\n"
            "   abhishek | abhishek123@gmail.com\n"
            "or type 'IN FILE' if you have updated data in a docs file: "
        ).strip()

        # Load new data from user or file
        new_data = []
        if user_input.lower() == "in file":
            if not state.doc_text:
                print("⚠️ No file data found in state. Please load the document first.")
                return state
            new_data = [t.strip() for t in state.doc_text if t.strip()]
        else:
            if "|" not in user_input:
                print("❌ Invalid format. Use 'name | email'.")
                return state
            new_data = [user_input]

        # ✅ Fetch existing data to prevent duplicates
        try:
            existing_texts = set()
            cursor = ""
            while True:
                query_result = index.query(
                    vector=[0.0] * 3072,  # dummy vector, just to fetch metadata
                    namespace=state.nameSpaces,
                    top_k=100,
                    include_metadata=True,
                    filter=None,
                    include_values=False,
                    start_cursor=cursor or None
                )
                for match in query_result.get("matches", []):
                    if match.get("metadata") and "text" in match["metadata"]:
                        existing_texts.add(match["metadata"]["text"])
                cursor = query_result.get("next_cursor")
                if not cursor:
                    break
        except Exception as e:
            print(f"⚠️ Could not fetch existing data: {e}")
            existing_texts = set()

        # ✅ Filter out duplicates
        unique_data = [d for d in new_data if d not in existing_texts]
        if not unique_data:
            print("⚠️ No new unique data found. Nothing to upsert.")
            return state

        # ✅ Store unique data in state so embed_and_upsert() can use it
        state.doc_text = unique_data
        print(f"📎 Found {len(unique_data)} unique records to append.")
    else:
        print("❌ Invalid option. Please choose (E)rase or (A)ppend.")
        return state

    state.index = index
    return state


def embed_and_upsert(state: GmailAutomateState):
    text_list = [t.strip() for t in state.doc_text if t.strip()]
    if not text_list:
        return state

    try:
        vectors = embed_model.embed_documents(text_list)  # Batch embedding
    except Exception as e:
        print(f"⚠️ Embedding failed: {e}")
        return state

    for text, vector in zip(text_list, vectors):
        vector_dict = {
            "id": f"vec-{os.urandom(4).hex()}",
            "values": vector,
            "metadata": {"text": text}
                    }
        print("✅ upsert with namespace as a parameter")
        state.index.upsert(vectors=[vector_dict], namespace=state.nameSpaces)
    return state
def select_or_create_index(state: GmailAutomateState):
    indexes = pc.list_indexes()
    existing_index_names = [idx['name'] for idx in indexes]

    state.new_index_auto_filled = False  # flag to track auto-upsert

    print("Available indexes:")
    for i, idx in enumerate(indexes, start=1):
        print(f"{i}. {idx['name']}")

    while True:
        user_input = input("Enter index number, index name, or type NEW to create a new one: ").strip()

        if user_input in existing_index_names:
            print(f"✅ Selected existing index: {user_input}")
            state.index_name = user_input
            break

        elif user_input.lower() == "new":
            new_index_name = input("Enter new index name: ").strip()
            if new_index_name in existing_index_names:
                print(f"ℹ️ Index '{new_index_name}' already exists. Selecting it instead.")
                state.index_name = new_index_name
            else:
                from pinecone.models import ServerlessSpec
                pc.create_index(
                    name=new_index_name,
                    dimension=3072,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
                print(f"✅ Created new index: {new_index_name}")
                state.index_name = new_index_name
                state.index = pc.Index(new_index_name)

                # ✅ Namespace setup
                default_ns = state.nameSpaces if state.nameSpaces else "automate-email-pinecone"
                ns_input = input(f"Enter namespace to use (default: {default_ns}): ").strip()
                state.nameSpaces = ns_input if ns_input else default_ns

                # ✅ Auto upsert doc_text
                if state.doc_text:
                    print(f"📎 Found {len(state.doc_text)} records in document. Adding to '{new_index_name}' under namespace '{state.nameSpaces}'...")
                    try:
                        vectors = embed_model.embed_documents(state.doc_text)
                        for text, vector in zip(state.doc_text, vectors):
                            state.index.upsert(
                                vectors=[{
                                    "id": f"vec-{os.urandom(4).hex()}",
                                    "values": vector,
                                    "metadata": {"text": text}
                                }],
                                namespace=state.nameSpaces
                            )
                        print("✅ Document data successfully added to the new index!")
                        state.new_index_auto_filled = True  # mark flag
                    except Exception as e:
                        print(f"⚠️ Failed to embed/upsert document data: {e}")
                else:
                    print("ℹ️ No document text found in state. Skipping auto-upsert.")

            break

        elif user_input.isdigit() and 1 <= int(user_input) <= len(indexes):
            selected_index = existing_index_names[int(user_input) - 1]
            print(f"✅ Selected index: {selected_index}")
            state.index_name = selected_index
            break

        else:
            print("❌ Invalid input. Please type a valid index number, existing index name, or 'NEW'.")

    if not hasattr(state, "index") or state.index is None:
        state.index = pc.Index(state.index_name)

    if not state.nameSpaces:
        default_ns = "automate-email-pinecone"
        ns_input = input(f"Enter namespace to use (default: {default_ns}): ").strip()
        state.nameSpaces = ns_input if ns_input else default_ns

    return state
