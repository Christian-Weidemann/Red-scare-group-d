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
            if (u in reds) != (v in reds): #works like XOR so it needs to be alternating to be a different colour
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
    return False


graphs = load_all()
true_count = 0
false_count = 0
results_list = []
for filename, graph in graphs.items():
    reds = graph.red
    result = bfs(graph,reds)
    results_list.append([filename,result])
    print(f"{filename}, {result}")
#    if result == True:
        #print(f"graph {filename} has alternating path: true")
#        true_count += 1
#    else:
        #print(f"graph {filename} has NO alternating path: false")
#        false_count +=1
#print(f"number of paths that can be reached when alternating colors {true_count}")
#print(f"number of paths that can NOT be reached when alternating colors {false_count}")
#print(results_list)