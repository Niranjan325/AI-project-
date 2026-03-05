from collections import deque
from typing import List, Set, Tuple, Dict, Optional
import time

class SearchStrategies:
    """
    Implementation of BFS and DFS search strategies with 4 classic problems:
    1. Tic-Tac-Toe
    2. Eight Queens
    3. Milk and Water Jug Problem  
    4. Missionaries and Cannibals
    """
    
    def __init__(self):
        self.nodes_explored = 0
        self.path = []
    
    def bfs(self, start_state, goal_test, get_successors):
        """Generic BFS implementation"""
        self.nodes_explored = 0
        queue = deque([(start_state, [])])
        visited = {str(start_state)}
        
        while queue:
            state, path = queue.popleft()
            self.nodes_explored += 1
            
            if goal_test(state):
                return path + [state], self.nodes_explored
            
            for successor in get_successors(state):
                successor_str = str(successor)
                if successor_str not in visited:
                    visited.add(successor_str)
                    queue.append((successor, path + [state]))
        
        return None, self.nodes_explored
    
    def dfs(self, start_state, goal_test, get_successors, max_depth=100):
        """Generic DFS implementation with depth limit"""
        self.nodes_explored = 0
        stack = [(start_state, [], 0)]
        visited = set()
        
        while stack:
            state, path, depth = stack.pop()
            state_str = str(state)
            
            if state_str in visited or depth > max_depth:
                continue
            
            visited.add(state_str)
            self.nodes_explored += 1
            
            if goal_test(state):
                return path + [state], self.nodes_explored
            
            for successor in get_successors(state):
                if str(successor) not in visited:
                    stack.append((successor, path + [state], depth + 1))
        
        return None, self.nodes_explored

# Problem 1: Tic-Tac-Toe
class TicTacToe:
    def __init__(self):
        self.searcher = SearchStrategies()
    
    def is_winner(self, board, player):
        # Check rows, columns, diagonals
        for i in range(3):
            if all(board[i][j] == player for j in range(3)):
                return True
            if all(board[j][i] == player for j in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)):
            return True
        if all(board[i][2-i] == player for i in range(3)):
            return True
        return False
    
    def get_successors(self, state):
        board, player = state
        successors = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    new_board = [row[:] for row in board]
                    new_board[i][j] = player
                    next_player = 2 if player == 1 else 1
                    successors.append((new_board, next_player))
        return successors
    
    def solve_bfs(self, start_board):
        start_state = (start_board, 1)
        goal = lambda s: self.is_winner(s[0], 1)
        return self.searcher.bfs(start_state, goal, self.get_successors)

# Problem 2: Eight Queens
class EightQueens:
    def __init__(self):
        self.searcher = SearchStrategies()
    
    def is_safe(self, board, row, col):
        # Check column
        for i in range(row):
            if board[i] == col:
                return False
            # Check diagonals
            if abs(board[i] - col) == abs(i - row):
                return False
        return True
    
    def get_successors(self, state):
        board, row = state
        if row >= 8:
            return []
        
        successors = []
        for col in range(8):
            if self.is_safe(board, row, col):
                new_board = board + [col]
                successors.append((new_board, row + 1))
        return successors
    
    def solve_bfs(self):
        start = ([], 0)
        goal = lambda s: len(s[0]) == 8
        return self.searcher.bfs(start, goal, self.get_successors)
    
    def solve_dfs(self):
        start = ([], 0)
        goal = lambda s: len(s[0]) == 8
        return self.searcher.dfs(start, goal, self.get_successors)

# Problem 3: Milk and Water Jug Problem
class WaterJugProblem:
    def __init__(self, jug1_capacity=4, jug2_capacity=3, target=2):
        self.jug1_cap = jug1_capacity
        self.jug2_cap = jug2_capacity
        self.target = target
        self.searcher = SearchStrategies()
    
    def goal_test(self, state):
        jug1, jug2 = state
        return jug1 == self.target or jug2 == self.target
    
    def get_successors(self, state):
        jug1, jug2 = state
        successors = []
        
        # Fill jug1
        successors.append((self.jug1_cap, jug2))
        # Fill jug2
        successors.append((jug1, self.jug2_cap))
        # Empty jug1
        successors.append((0, jug2))
        # Empty jug2
        successors.append((jug1, 0))
        # Pour jug1 -> jug2
        pour = min(jug1, self.jug2_cap - jug2)
        successors.append((jug1 - pour, jug2 + pour))
        # Pour jug2 -> jug1
        pour = min(jug2, self.jug1_cap - jug1)
        successors.append((jug1 + pour, jug2 - pour))
        
        return successors
    
    def solve_bfs(self):
        start = (0, 0)
        return self.searcher.bfs(start, self.goal_test, self.get_successors)
    
    def solve_dfs(self):
        start = (0, 0)
        return self.searcher.dfs(start, self.goal_test, self.get_successors, max_depth=20)

# Problem 4: Missionaries and Cannibals
class MissionariesCannibals:
    def __init__(self):
        self.searcher = SearchStrategies()
    
    def is_valid(self, state):
        m_left, c_left, boat, m_right, c_right = state
        
        # Check bounds
        if m_left < 0 or c_left < 0 or m_right < 0 or c_right < 0:
            return False
        if m_left > 3 or c_left > 3 or m_right > 3 or c_right > 3:
            return False
        
        # Missionaries can't be outnumbered
        if m_left > 0 and m_left < c_left:
            return False
        if m_right > 0 and m_right < c_right:
            return False
        
        return True
    
    def goal_test(self, state):
        return state == (0, 0, 0, 3, 3)
    
    def get_successors(self, state):
        m_left, c_left, boat, m_right, c_right = state
        successors = []
        
        # Possible moves: 1M, 2M, 1C, 2C, 1M1C
        moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
        
        if boat == 1:  # Boat on left
            for m, c in moves:
                new_state = (m_left - m, c_left - c, 0, m_right + m, c_right + c)
                if self.is_valid(new_state):
                    successors.append(new_state)
        else:  # Boat on right
            for m, c in moves:
                new_state = (m_left + m, c_left + c, 1, m_right - m, c_right - c)
                if self.is_valid(new_state):
                    successors.append(new_state)
        
        return successors
    
    def solve_bfs(self):
        start = (3, 3, 1, 0, 0)
        return self.searcher.bfs(start, self.goal_test, self.get_successors)
    
    def solve_dfs(self):
        start = (3, 3, 1, 0, 0)
        return self.searcher.dfs(start, self.goal_test, self.get_successors, max_depth=30)

# Testing and Performance Comparison
if __name__ == "__main__":
    print("="*60)
    print("BFS vs DFS Performance Comparison")
    print("="*60)
    
    # Test 1: Eight Queens Problem
    print("\n1. EIGHT QUEENS PROBLEM")
    print("-" * 60)
    eq = EightQueens()
    
    start = time.time()
    solution_bfs, nodes_bfs = eq.solve_bfs()
    time_bfs = time.time() - start
    
    start = time.time()
    solution_dfs, nodes_dfs = eq.solve_dfs()
    time_dfs = time.time() - start
    
    print(f"BFS: Nodes explored = {nodes_bfs}, Time = {time_bfs:.4f}s")
    print(f"DFS: Nodes explored = {nodes_dfs}, Time = {time_dfs:.4f}s")
    if solution_dfs:
        print(f"DFS Solution: {solution_dfs[-1][0]}")
    
    # Test 2: Water Jug Problem
    print("\n2. WATER JUG PROBLEM (4L, 3L -> 2L)")
    print("-" * 60)
    wj = WaterJugProblem(4, 3, 2)
    
    start = time.time()
    solution_bfs, nodes_bfs = wj.solve_bfs()
    time_bfs = time.time() - start
    
    start = time.time()
    solution_dfs, nodes_dfs = wj.solve_dfs()
    time_dfs = time.time() - start
    
    print(f"BFS: Nodes explored = {nodes_bfs}, Time = {time_bfs:.4f}s")
    print(f"DFS: Nodes explored = {nodes_dfs}, Time = {time_dfs:.4f}s")
    if solution_bfs:
        print(f"BFS Solution path length: {len(solution_bfs)}")
        print(f"Steps: {solution_bfs}")
    
    # Test 3: Missionaries and Cannibals
    print("\n3. MISSIONARIES AND CANNIBALS PROBLEM")
    print("-" * 60)
    mc = MissionariesCannibals()
    
    start = time.time()
    solution_bfs, nodes_bfs = mc.solve_bfs()
    time_bfs = time.time() - start
    
    start = time.time()
    solution_dfs, nodes_dfs = mc.solve_dfs()
    time_dfs = time.time() - start
    
    print(f"BFS: Nodes explored = {nodes_bfs}, Time = {time_bfs:.4f}s")
    print(f"DFS: Nodes explored = {nodes_dfs}, Time = {time_dfs:.4f}s")
    if solution_bfs:
        print(f"BFS Solution path length: {len(solution_bfs)}")
    
    # Performance Summary
    print("\n" + "="*60)
    print("ANALYSIS")
    print("="*60)
    print("BFS Characteristics:")
    print("  ✔ Guarantees shortest path")
    print("  ✔ Complete (finds solution if exists)")
    print("  ✘ Uses more memory (stores all nodes at current level)")
    print("\nDFS Characteristics:")
    print("  ✔ Uses less memory (stack-based)")
    print("  ✔ Faster for deep solutions")
    print("  ✘ May not find shortest path")
    print("  ✘ Can get stuck in infinite loops (needs depth limit)")
