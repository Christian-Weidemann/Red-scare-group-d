from graph_loader import DATA_DIR, Graph, load_graph, load_all
from collections import deque

def bfs(graph, reds):
    start = graph.s
    end = graph.t
    visited =  {start}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        if u == end:
            return True
        for v in graph.adj[u]:
            if (u in reds) != (v in reds):
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
    return False

graphs = load_all()
true_count = 0
false_count = 0
for filename, graph in graphs.items():
    reds = graph.red
    result = bfs(graph,reds)
    if result == True:
        print('true')
        true_count += 1
    else:
        print('false')
        false_count +=1
print(f"number of paths that can be reached when alternating colors {true_count}")
print(f"number of paths that can NOT be reached when alternating colors {false_count}")