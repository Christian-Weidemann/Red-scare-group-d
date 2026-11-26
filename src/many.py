"""Many: maximum number of red vertices on a simple s-t path.
Moved from notebooks/Many.ipynb so run_all.py can import it.
"""
from collections import deque
from math import inf

from graph_loader_few import Graph

"""
Written by Claude (Anthropic) in October 2026.
"""

def solve_many(g: Graph, time_limit: float = 5.0) -> dict:
    """Maximum number of red vertices on any simple s-t path.

    Returns {'answer': int | None, 'exact': bool, 'method': str}.
    answer is -1 if no s-t path exists.
    If brute force times out, answer is the best found so far (a lower bound)
    and exact is False. answer is None if no path was found in time.
    """
    if g.s == g.t:
        return {'answer': int(g.s in g.red), 'exact': True, 'method': 's == t'}
    if g.directed:
        return _solve_directed(g, time_limit)
    return _solve_undirected(g, time_limit)


# ---------- Directed ----------

def _solve_directed(g: Graph, time_limit: float) -> dict:
    out = [[v for v, _ in g.adj[u]] for u in range(g.n)]
    inn = [[] for _ in range(g.n)]
    for u in range(g.n):
        for v in out[u]:
            inn[v].append(u)

    from_s = _reachable(g.s, out)
    if g.t not in from_s:
        return {'answer': -1, 'exact': True, 'method': 'no path'}
    relevant = from_s & _reachable(g.t, inn)       # on some s-t walk

    # Arcs inside the relevant part, negative weights, no self-loops
    arcs = [(u, v, -abs(w)) for u in relevant for v, w in g.adj[u]
            if v in relevant and v != u]
    sub_out = {u: [] for u in relevant}
    sub_in = {u: [] for u in relevant}
    for u, v, _ in arcs:
        sub_out[u].append(v)
        sub_in[v].append(u)

    # All weights are <= 0, so a negative cycle exists
    # if and only if a negative arc lies inside a strongly connected component
    comp = _scc(relevant, sub_out, sub_in)
    has_neg_cycle = any(w < 0 and comp[u] == comp[v] for u, v, w in arcs)

    if not has_neg_cycle:
        path = _bellman_ford_path(relevant, arcs, g.s, g.t)
        return {'answer': sum(v in g.red for v in path), 'exact': True,
                'method': 'bellman-ford'}

    return {"answer" : None, "exact" : False, "method" : "brute force"}


def _bellman_ford_path(nodes, arcs, s, t) -> list[int]:
    """Shortest s-t path. Assumes no negative cycles."""
    dist = {v: inf for v in nodes}
    pred = {}
    dist[s] = 0
    for _ in range(len(nodes) - 1):
        changed = False
        for u, v, w in arcs:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                changed = True
        if not changed:                            # stop early when nothing changes
            break
    path = [t]
    while path[-1] != s:
        path.append(pred[path[-1]])
    return path[::-1]


def _scc(nodes, out, inn) -> dict[int, int]:
    """Kosaraju: vertex -> id of its strongly connected component."""
    order, seen = [], set()
    for root in nodes:
        if root in seen:
            continue
        seen.add(root)
        stack = [(root, iter(out[root]))]
        while stack:
            u, it = stack[-1]
            for v in it:
                if v not in seen:
                    seen.add(v)
                    stack.append((v, iter(out[v])))
                    break
            else:
                stack.pop()
                order.append(u)
    comp = {}
    for root in reversed(order):
        if root in comp:
            continue
        comp[root] = root
        stack = [root]
        while stack:
            u = stack.pop()
            for v in inn[u]:
                if v not in comp:
                    comp[v] = root
                    stack.append(v)
    return comp


# ---------- Undirected ----------

def _solve_undirected(g: Graph, time_limit: float) -> dict:
    # Plain neighbour sets: no weights, self-loops or parallel edges
    nbrs = [{v for v, _ in g.adj[u] if v != u} for u in range(g.n)]
    component = _reachable(g.s, nbrs)
    if g.t not in component:
        return {'answer': -1, 'exact': True, 'method': 'no path'}

    # The vertices on some s-t path are exactly the block (biconnected component)
    # that contains the edge s-t, after adding that edge
    with_st = {u: set(nbrs[u]) for u in component}
    with_st[g.s].add(g.t)
    with_st[g.t].add(g.s)
    blocks, _ = _blocks(with_st, g.s)
    relevant = next(b for b in blocks if g.s in b and g.t in b)

    sub = {u: nbrs[u] & relevant for u in relevant}
    red = g.red & relevant

    # Cut vertices of sub lie on every s-t path. If every relevant red vertex
    # is s, t or a cut vertex, all s-t paths have the same red count.
    _, cut = _blocks(sub, g.s)
    if red <= cut | {g.s, g.t}:
        return {'answer': len(red), 'exact': True, 'method': 'forced'}

    return {"answer" : None, "exact" : False, "method" : "brute force"}


def _blocks(nbrs: dict[int, set[int]], root: int):
    """Tarjan: blocks (as vertex sets) and cut vertices of the component of root.
    nbrs must have no parallel edges or self-loops."""
    disc, low = {root: 0}, {root: 0}
    timer = 1
    edge_stack, blocks, cut = [], [], set()
    root_children = 0
    stack = [(root, -1, iter(nbrs[root]))]
    while stack:
        u, parent, it = stack[-1]
        for v in it:
            if v == parent:
                continue
            if v not in disc:                      # tree edge
                edge_stack.append((u, v))
                disc[v] = low[v] = timer
                timer += 1
                stack.append((v, u, iter(nbrs[v])))
                break
            if disc[v] < disc[u]:                  # back edge to an ancestor
                edge_stack.append((u, v))
                low[u] = min(low[u], disc[v])
        else:                                      # u is finished
            stack.pop()
            if stack:
                p = stack[-1][0]
                low[p] = min(low[p], low[u])
                if low[u] >= disc[p]:              # p separates u's subtree
                    if p == root:
                        root_children += 1
                    else:
                        cut.add(p)
                    block = set()
                    while True:
                        a, b = edge_stack.pop()
                        block.update((a, b))
                        if (a, b) == (p, u):
                            break
                    blocks.append(block)
    if root_children > 1:
        cut.add(root)
    return blocks, cut


# ---------- Shared ----------

def _reachable(start: int, nbrs) -> set[int]:
    seen = {start}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in nbrs[u]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    return seen


