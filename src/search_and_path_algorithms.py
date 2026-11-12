

from collections import deque

def bfs(graph, S, par, dist):
    """
    Modified bfs to store the parent of nodes along with the
    distance from source node
    Source: https://www.geeksforgeeks.org/dsa/shortest-path-unweighted-graph/
    """
    
    # queue to store the nodes in the order they are
    # visited
    q = deque()
    
    # Mark the distance of the source node as 0
    dist[S] = 0
    
    # Push the source node to the queue
    q.append(S)

    # Iterate till the queue is not empty
    while q:
        # Pop the node at the front of the queue
        node = q.popleft()
        
        # Explore all the neighbours of the current node
        for neighbour in graph[node]:
            
            # Check if the neighbouring node is not visited
            if dist[neighbour] == 1e9:
                
                # Mark the current node as the parent of
                # the neighbouring node
                par[neighbour] = node
                
                # Mark the distance of the neighbouring
                # node as distance of the current node + 1
                dist[neighbour] = dist[node] + 1
                
                # Insert the neighbouring node to the queue
                q.append(neighbour)


def printShortestDistance(graph):
    """
    # Function to print the shortest distance between source
    # vertex and destination vertex
    Source: https://www.geeksforgeeks.org/dsa/shortest-path-unweighted-graph/
    """

    start_ind = graph.index[graph.names[graph.s]]
    target_ind = graph.index[graph.names[graph.t]]

    if start_ind in graph.red or target_ind in graph.red:
        return -1

    S = graph.s
    D = graph.t
    V = graph.n

    graph = graph.adj


    # par[] array stores the parent of nodes
    par = [-1] * V

    # dist[] array stores distance of nodes from S
    dist = [1e9] * V

    # function call to find the distance of all nodes and
    # their parent nodes
    bfs(graph, S, par, dist)

    if dist[D] == 1e9:
        return -1

    # vector path stores the shortest path
    path = []
    currentNode = D
    path.append(D)
    while par[currentNode]!= -1:
        path.append(par[currentNode])
        currentNode = par[currentNode]

    return len(path)
