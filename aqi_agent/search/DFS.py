import time
from missionaries import INITIAL_STATE, GOAL_STATE, get_successors


def dfs():
    stack = []
    stack.append((INITIAL_STATE, [INITIAL_STATE]))
    visited = set()

    while stack:
        current_state, path = stack.pop()

        if current_state == GOAL_STATE:
            return path

        if current_state not in visited:
            visited.add(current_state)

            for successor in get_successors(current_state):
                if successor not in visited:
                    stack.append((successor, path + [successor]))

    return None


if __name__ == "__main__":
    start_time = time.time()

    solution = dfs()

    end_time = time.time()

    if solution:
        print("DFS Solution Found!")
        for step in solution:
            print(step)
        print("Total Steps:", len(solution) - 1)
        print("Execution Time:", end_time - start_time, "seconds")
    else:
        print("No solution found.")
        print("Execution Time:", end_time - start_time, "seconds")
