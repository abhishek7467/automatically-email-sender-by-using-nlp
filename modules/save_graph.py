import subprocess
import os
def graph_to_png(app):
    mermaid_code = app.get_graph().draw_mermaid()
    mermaid_file = "graph.mmd"
    with open(mermaid_file, "w") as f:
        f.write(mermaid_code)
    output_png = "graph.png"
    try:
        subprocess.run(["mmdc", "-i", mermaid_file, "-o", output_png], check=True)
        print(f"Diagram saved successfully as {output_png}")
    except subprocess.CalledProcessError as e:
        print("Error generating PNG:", e)
    finally:
        if os.path.exists(mermaid_file):
            os.remove(mermaid_file)
