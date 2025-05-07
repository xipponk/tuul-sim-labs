import copy

INFINITY = float('inf')

# ANSI color codes
RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"

def read_graph():
    print(f"{CYAN} Enter your graph (format: node1 node2 cost). Type 'done' to finish:{RESET}\n")
    graph = {}

    while True:
        line = input("Edge: ").strip()
        if line.lower() == 'done':
            break
        parts = line.split()
        if len(parts) != 3:
            print(f"{RED} Invalid format. Use: A B 4{RESET}")
            continue
        u, v, cost = parts[0], parts[1], float(parts[2])
        if u not in graph:
            graph[u] = {}
        if v not in graph:
            graph[v] = {}
        graph[u][v] = cost
        graph[v][u] = cost  # Undirected graph

    return graph

def init_distance_vectors(graph):
    nodes = list(graph.keys())
    dv = {}
    for node in nodes:
        dv[node] = {dst: (0 if dst == node else (graph[node][dst] if dst in graph[node] else INFINITY)) for dst in nodes}
    return dv

def print_distance_vectors(dv, round_num, changed_cells=None):
    print(f"\n{BOLD}{YELLOW} Distance Vector Tables (Round {round_num}){RESET}")
    for node in sorted(dv):
        print(f"{BOLD}Node {node}:{RESET} ", end='')
        for dest in sorted(dv[node]):
            cost = dv[node][dest]
            val = f"{int(cost)}" if cost != INFINITY else "∞"

            if changed_cells and (node, dest) in changed_cells:
                print(f"{GREEN}D[{dest}]={val}{RESET} ", end='')
            else:
                print(f"D[{dest}]={val} ", end='')
        print()

def distance_vector_step(graph, dv):
    updated = False
    changed_cells = set()
    nodes = list(graph.keys())
    new_dv = copy.deepcopy(dv)

    for x in nodes:
        for v in graph[x]:  # each neighbor
            for y in nodes:  # each destination
                alt = graph[x][v] + dv[v][y]
                if alt < new_dv[x][y]:
                    new_dv[x][y] = alt
                    changed_cells.add((x, y))
                    updated = True
    return new_dv, updated, changed_cells

# === Main ===
if __name__ == "__main__":
    graph = read_graph()
    dv = init_distance_vectors(graph)

    round_num = 0
    while True:
        round_num += 1
        print_distance_vectors(dv, round_num)

        input(f"{CYAN}Press Enter for next round...{RESET}")
        new_dv, changed, changed_cells = distance_vector_step(graph, dv)
        print_distance_vectors(new_dv, round_num + 0.1, changed_cells)

        if not changed:
            print(f"\n{GREEN} Converged! No changes in this round.{RESET}")
            break
        dv = new_dv