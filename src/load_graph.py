"""Load graph files of the form:

    n m r
    s t
    <n vertex lines>   (names in R end with " *")
    <m edge lines>     ("u -- v" undirected, "u -> v" directed)

    AI usage:
    - Created by Claude (Anthropic) in november 2026
"""
from dataclasses import dataclass, field
from pathlib import Path

# <project>/src/load_graph.py -> <project>/problem_and_data/data
DATA_DIR = Path(__file__).resolve().parent.parent / "problem_and_data" / "data"


@dataclass
class Graph:
    names: list[str]                 # index -> vertex name
    index: dict[str, int]            # vertex name -> index
    red: set[int]                    # indices of vertices in R
    s: int
    t: int
    adj: list[list[int]]             # out-neighbours (both ways for "--")
    edges: list[tuple[int, int, bool]] = field(default_factory=list)  # (u, v, directed)
    directed: bool = False           # True if any edge is "->"

    @property
    def n(self) -> int:
        return len(self.names)

    @property
    def m(self) -> int:
        return len(self.edges)


def load_graph(path: str | Path) -> Graph:
    lines = [ln.strip() for ln in Path(path).read_text().splitlines()]
    lines = [ln for ln in lines if ln]          # skip blank lines
    it = iter(lines)

    n, m, r = map(int, next(it).split())
    s_name, t_name = next(it).split()

    names: list[str] = []
    red_names: set[str] = set()
    for _ in range(n):
        parts = next(it).split()
        names.append(parts[0])
        if len(parts) > 1 and parts[1] == "*":
            red_names.add(parts[0])

    index = {name: i for i, name in enumerate(names)}
    adj: list[list[int]] = [[] for _ in range(n)]
    edges: list[tuple[int, int, bool]] = []
    directed = False

    for _ in range(m):
        u_name, op, v_name = next(it).split()
        u, v = index[u_name], index[v_name]
        if op == "->":
            adj[u].append(v)
            edges.append((u, v, True))
            directed = True
        elif op == "--":
            adj[u].append(v)
            adj[v].append(u)
            edges.append((u, v, False))
        else:
            raise ValueError(f"Unknown edge operator {op!r} in {path}")

    red = {index[x] for x in red_names}
    if len(red) != r:
        raise ValueError(f"{path}: header says r={r}, found {len(red)} vertices in R")

    return Graph(names, index, red, index[s_name], index[t_name], adj, edges, directed)


def load_all(folder: str | Path = DATA_DIR) -> dict[str, Graph]:
    """Load every .txt file in the folder, keyed by file name."""
    return {p.name: load_graph(p) for p in sorted(Path(folder).glob("*.txt"))}


if __name__ == "__main__":
    import sys
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA_DIR
    files = [target] if target.is_file() else sorted(target.glob("*.txt"))
    if not files:
        print(f"No .txt files found in {target}")
    for p in files:
        g = load_graph(p)
        print(f"{p.name}: n={g.n} m={g.m} |R|={len(g.red)} "
              f"s={g.names[g.s]} t={g.names[g.t]} directed={g.directed}")