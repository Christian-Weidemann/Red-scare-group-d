"""None: shortest s-t path that avoids red vertices (s and t may be red).
Moved from notebooks/None.ipynb so run_all.py can import it.
"""
from graph_loader import Graph
from search_and_path_algorithms import printShortestDistance


def remove_red(g: Graph, keep_st: bool = True) -> Graph:
    """Return a copy of g without the vertices in R and their edges.

    If keep_st is True, s and t are kept even when they are red.
    Written by Claude (Anthropic)
    """
    keep = [v for v in range(g.n)
            if v not in g.red or (keep_st and v in (g.s, g.t))]
    new_id = {old: new for new, old in enumerate(keep)}   # old index -> new index

    names = [g.names[v] for v in keep]
    adj = [[] for _ in keep]
    edges = []
    for u, v, directed in g.edges:
        if u in new_id and v in new_id:                   # both ends survive
            nu, nv = new_id[u], new_id[v]
            edges.append((nu, nv, directed))
            adj[nu].append(nv)
            if not directed:
                adj[nv].append(nu)

    return Graph(
        names=names,
        index={name: i for i, name in enumerate(names)},
        red={new_id[v] for v in g.red if v in new_id},    # only red s or t can remain
        s=new_id.get(g.s, -1),                            # -1 if s was removed
        t=new_id.get(g.t, -1),
        adj=adj,
        edges=edges,
        directed=g.directed,
        file_path=g.file_path,
    )


def solve_none(g: Graph) -> int:
    """Length of the shortest red-free s-t path, or -1 if there is none."""
    return printShortestDistance(remove_red(g))
