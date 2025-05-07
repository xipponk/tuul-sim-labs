import heapq

def dijkstra_interactive(graph, start):
    D = {node: float('inf') for node in graph}
    D[start] = 0
    previous = {node: None for node in graph}
    visited = set()
    queue = [(0, start)]

    print(f"\n🔹 Start from node: {start}")
    input("Press Enter to begin...")

    while queue:
        (dist_u, u) = heapq.heappop(queue)
        if u in visited:
            continue
        visited.add(u)
        print(f"\n Add node {u} to N'")
        print("   Current D values:")
        for node in D:
            val = f"{D[node]}" if D[node] != float('inf') else "∞"
            print(f"   D[{node}] = {val}")

        for v in graph[u]:
            if v not in visited:
                new_dist = D[u] + graph[u][v]
                if new_dist < D[v]:
                    D[v] = new_dist
                    previous[v] = u
                    heapq.heappush(queue, (new_dist, v))
                    print(f"   Updated D[{v}] = {new_dist} via {u}")
        
        input("Press Enter for next step...")

    return D, previous

def reconstruct_path(previous, target):
    path = []
    while target is not None:
        path.insert(0, target)
        target = previous[target]
    return path

def read_graph_from_input():
    print("Please Enter your graph (one edge per line, format: node1 node2 cost)")
    print("    Type 'done' to finish input.\n")

    graph = {}

    while True:
        line = input("Edge: ").strip()
        if line.lower() == 'done':
            break
        parts = line.split()
        if len(parts) != 3:
            print("Invalid input. Please enter in format: node1 node2 cost")
            continue
        u, v, cost = parts[0], parts[1], float(parts[2])
        if u not in graph:
            graph[u] = {}
        if v not in graph:
            graph[v] = {}
        graph[u][v] = cost
        graph[v][u] = cost  # assume undirected

    return graph

# === Main ===
if __name__ == "__main__":
    graph = read_graph_from_input()
    print("\n Graph loaded.")
    print("Nodes:", ', '.join(graph.keys()))
    start_node = input("Enter start node: ").strip()

    if start_node not in graph:
        print("Invalid start node. Exiting.")
    else:
        D, previous = dijkstra_interactive(graph, start_node)

        print("\n Final shortest distances:")
        for node in sorted(D):
            print(f"   D[{node}] = {D[node]}")

        print("\n Shortest paths from start to each node:")
        for node in sorted(graph):
            path = reconstruct_path(previous, node)
            print(f"   {start_node} → {node}: {' → '.join(path)}")