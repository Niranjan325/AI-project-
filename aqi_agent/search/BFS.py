import time
from collections import deque
from missionaries import INITIAL_STATE, GOAL_STATE, get_successors


def bfs():
    queue = deque()
    queue.append((INITIAL_STATE, [INITIAL_STATE]))
    visited = set()

    while queue:
        current_state, path = queue.popleft()

        if current_state == GOAL_STATE:
            return path

        visited.add(current_state)

        for successor in get_successors(current_state):
            if successor not in visited:
                queue.append((successor, path + [successor]))

    return None


if __name__ == "__main__":
    start_time = time.time()

    solution = bfs()

    end_time = time.time()

    if solution:
        print("BFS Solution Found!")
        for step in solution:
            print(step)
        print("Total Steps:", len(solution) - 1)
        print("Execution Time:", end_time - start_time, "seconds")
    else:
        print("No solution found.")
        print("Execution Time:", end_time - start_time, "seconds")
