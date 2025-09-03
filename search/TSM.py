import sys
from itertools import combinations


def tsp_dp_with_path(graph):
    n = len(graph)
    dp = {}
    parent = {}

    # Initialize base cases
    for i in range(1, n):
        dp[(1 << i, i)] = graph[0][i]
        parent[(1 << i, i)] = 0

    # Build DP table
    for r in range(2, n):
        for subset in combinations(range(1, n), r):
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            for k in subset:
                prev = bits & ~(1 << k)
                min_cost = sys.maxsize
                min_prev_city = -1

                for m in subset:
                    if m == k:
                        continue
                    if (prev, m) in dp:
                        cost = dp[(prev, m)] + graph[m][k]
                        if cost < min_cost:
                            min_cost = cost
                            min_prev_city = m

                dp[(bits, k)] = min_cost
                parent[(bits, k)] = min_prev_city

    # Final step: return to start (0)
    full_mask = (1 << n) - 2
    min_cost = sys.maxsize
    last_city = -1

    for k in range(1, n):
        cost = dp[(full_mask, k)] + graph[k][0]
        if cost < min_cost:
            min_cost = cost
            last_city = k

    # Recover path
    path = [0]
    mask = full_mask
    current = last_city

    for _ in range(n - 1):
        path.append(current)
        next_city = parent[(mask, current)]
        mask = mask & ~(1 << current)
        current = next_city

    path.append(0)  # return to start
    path.reverse()

    return min_cost, path

graph = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

cost, path = tsp_dp_with_path(graph)
print("Minimum Cost:", cost)
print("Best Path:", path)

