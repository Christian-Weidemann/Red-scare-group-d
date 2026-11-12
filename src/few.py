import graph_loader_few as glf
import search_and_path_algorithms as spa
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "problem_and_data" / "data"

GRAPH_TYPE_PREFIXES = {
    "Common word": "common",
    "Rusty word": "rusty",
    "Grids": "grid",
    "Walls": "wall",
    "Random": ["smallworld", "gnm", "bht"],
    "Increasing numbers": "increase",
}
DEFAULT_TYPE = "Individual"  # any file that matches no prefix

if __name__ == "__main__":
    import sys

    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA_DIR
    files = [target] if target.is_file() else sorted(target.glob("*.txt"))
    df = pd.DataFrame()
    if not files:
        print(f"No .txt files found in {target}")
    for p in files:
        g = glf.load_graph(p)
        distances = spa.dijkstra(g.adj, g.s)
        if g.s in g.red and g.t in g.red:
            cost = distances[g.t] / 2 + 1
        else:
            cost = distances[g.t] / 2

        if cost != float("inf"):
            cost = round(cost)
        else:
            cost = -1
        # print(f"{p.name}: c = {cost} ")
        row = pd.DataFrame([{"Name": p.name, "cost": round(cost)}])
        df = pd.concat([df, row], ignore_index=True)
    df.to_csv("result_few.csv")
    # print(g.adj)
    # print(g.adj[0][0])
    # print(g.adj[0][0][0])
    # distances = spa.dijkstra(g.adj, g.s)
    # cost = distances[g.t] / 2
    # print(f"Shortest path cost: {cost}")
