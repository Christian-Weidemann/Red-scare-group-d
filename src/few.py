import graph_loader_few as glf
import search_and_path_algorithms as spa
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "problem_and_data" / "data"

GRAPH_TYPE_PREFIXES = {'Common word':'common', 'Rusty word': 'rusty', 
                       'Grids':'grid', 
                       'Walls': 'wall', 
                       'Random':['smallworld', 'gnm', 'bht'],
                       'Increasing numbers': 'increase'}
DEFAULT_TYPE = 'Individual'   # any file that matches no prefix




if __name__ == "__main__":
    import sys
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA_DIR
    files = [target] if target.is_file() else sorted(target.glob("*.txt"))
    if not files:
        print(f"No .txt files found in {target}")
    for p in files:
        g = glf.load_graph(p)
        print(f"{p.name}: n={g.n} m={g.m} |R|={len(g.red)} "
              f"s={g.names[g.s]} t={g.names[g.t]} directed={g.directed}")
    print(g.adj[0])
    print(g.adj[0][0])
    print(g.adj[0][0][0])
    distances = spa.dijkstra(g.edges, g.s)
    cost = distances[g.t]/2
    print(f"Shortest path cost: {cost}")
    
    