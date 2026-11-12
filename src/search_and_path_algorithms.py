import heapq

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


def dijkstra(adj, src):
    V = len(adj)

    # Min-heap storing {distance, vertex}
    pq = []

    # Initialize distances to infinity
    dist = [float('inf')] * V

    # Distance from source to itself is 0
    dist[src] = 0
    heapq.heappush(pq, (0, src))

    while pq:

        d, u = heapq.heappop(pq)

        # Skip outdated entries
        if d > dist[u]:
            continue

        # Traverse adjacent vertices
        for x in adj[u]:            
            v = x[0]
            weight = x[1]
            # Update distance if a shorter path is found
            if dist[v] > d + weight:
                dist[v] = d + weight
                heapq.heappush(pq, (dist[v], v))

    return dist


def printShortestDistance(graph):
    """
    # Function to print the shortest distance between source
    # vertex and destination vertex
    Source: https://www.geeksforgeeks.org/dsa/shortest-path-unweighted-graph/
    """

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
        print("Source and Destination are not connected")
        return

    # vector path stores the shortest path
    path = []
    currentNode = D
    path.append(D)
    while par[currentNode]!= -1:
        path.append(par[currentNode])
        currentNode = par[currentNode]

    # printing path from source to destination
    for i in range(len(path)-1, -1, -1):
        print(path[i], end=" ")