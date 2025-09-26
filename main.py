import argparse
import traceback
from modules.langgraph_work import main_graph

def run_app(option: str, query: str):
    try:
        app = main_graph()
        print("✅ App compiled successfully")
        result = app.invoke({"option": option, "query": query})
        print("🎯 Final result:", result)
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run LangGraph workflow from CLI")

    # Add CLI arguments
    parser.add_argument("--option", type=str, required=True, help="Workflow option (e.g., chat, data_store)")
    parser.add_argument("--query", type=str, required=False, default="", help="Query to process")

    args = parser.parse_args()

    # Run with parsed args
    run_app(option=args.option, query=args.query)



# # Chat mode with query
# python3 main.py --option chat --query "send a email to abhishek orange for requesting about my laptop is not working i need help of IT team."

# # Data store mode
# python main.py --option data_store

