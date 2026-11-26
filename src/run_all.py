"""Rebuild results.txt from scratch: one row per graph in problem_and_data/data.

Usage (from the repo root):  python src/run_all.py

Written by Claude (Anthropic) in October 2026.
"""
from pathlib import Path

import pandas as pd

import graph_loader
import graph_loader_few
from alternate_dmst_implementation import bfs as has_alternating_path
from few import few_cost
from many import solve_many
from none import solve_none
from some import has_some_red_path

RESULTS = Path(__file__).resolve().parent.parent / "results.txt"


def solve_all(path: Path) -> dict:
    g = graph_loader.load_graph(path)            # unweighted adjacency
    gw = graph_loader_few.load_graph(path)       # red-weighted adjacency (Few, Many)

    many = solve_many(gw)
    alternate = has_alternating_path(g, g.red)
    few = few_cost(gw)
    # Same shortcut as some.py: an alternating path or a path with >0 reds already proves Some
    some = True if alternate or few > 0 else has_some_red_path(g)

    return {
        "filename": path.name,
        "n": g.n,
        "None": solve_none(g),
        "Many": many["answer"] if many["exact"] else "?!",
        "Few": few,
        "Alternate": alternate,
        "Some": some,
    }


if __name__ == "__main__":
    rows = []
    for p in sorted(graph_loader.DATA_DIR.glob("*.txt")):
        print(p.name, flush=True)
        rows.append(solve_all(p))
    pd.DataFrame(rows).to_csv(RESULTS)
    print(f"Wrote {len(rows)} rows to {RESULTS}")
