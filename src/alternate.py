from graph_loader import DATA_DIR, Graph, load_graph
from collections import deque

def find_alternated_path(graph):
    parent = {graph.s:None}
    queue = deque([graph.s])

    while queue: 
        node = queue.popleft()
        if node == graph.t:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return True
        
        for neighbor in graph.adj[node]:
            if node in graph.red:
                if neighbor not in graph.red and neighbor not in parent:
                    parent[neighbor] = node
                    queue.append(neighbor)
            
            if node not in graph.red:
                if neighbor in graph.red and neighbor not in parent:
                    parent[neighbor] = node
                    queue.append(neighbor)
        
    return False
                

if __name__ == "__main__":

    files = DATA_DIR.glob("*txt")
    if not files:
        print("No text files found")

    else:
        print("The alternating paths for the following files") 
        for p in files: 
            graph = load_graph(p)
            result = find_alternated_path(graph)

            print(f"{result} for {p.name}")