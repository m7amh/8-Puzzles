import tkinter as tk
from tkinter import messagebox
from collections import deque
import heapq
import random
import math

class EightPuzzle:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.current_state = initial_state

    def goal_test(self, state):
        return state == [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def solve_bfs(self):
        frontier = deque([(self.initial_state, [])])
        explored = set()

        while frontier:
            state, path = frontier.popleft()
            explored.add(tuple(state))

            if self.goal_test(state):
                self.current_state = state
                self.update_gui()
                messagebox.showinfo("BFS", f"BFS found a solution in {len(path)} moves.")
                return

            for neighbor in self.neighbors(state):
                if tuple(neighbor) not in explored:
                    frontier.append((neighbor, path + [neighbor]))
                    self.current_state = neighbor
                    self.update_gui()

        messagebox.showinfo("BFS", "BFS did not find a solution.")

    def solve_dfs(self):
        frontier = [(self.initial_state, [])]
        explored = set()

        while frontier:
            state, path = frontier.pop()
            explored.add(tuple(state))

            if self.goal_test(state):
                self.current_state = state
                self.update_gui()
                messagebox.showinfo("DFS", f"DFS found a solution in {len(path)} moves.")
                return

            for neighbor in self.neighbors(state):
                if tuple(neighbor) not in explored:
                    frontier.append((neighbor, path + [neighbor]))
                    self.current_state = neighbor
                    self.update_gui()

        messagebox.showinfo("DFS", "DFS did not find a solution.")

    def solve_a_star(self):
        frontier = [(self.heuristic(self.initial_state), 0, self.initial_state, [])]
        explored = set()

        while frontier:
            _, cost, state, path = heapq.heappop(frontier)
            explored.add(tuple(state))

            if self.goal_test(state):
                self.current_state = state
                self.update_gui()
                messagebox.showinfo("A*", f"A* found a solution in {len(path)} moves.")
                return

            for neighbor in self.neighbors(state):
                if tuple(neighbor) not in explored:
                    new_cost = cost + 1
                    priority = new_cost + self.heuristic(neighbor)
                    heapq.heappush(frontier, (priority, new_cost, neighbor, path + [neighbor]))
                    self.current_state = neighbor
                    self.update_gui()

        messagebox.showinfo("A*", "A* did not find a solution.")

    def heuristic(self, state):
        # Manhattan Distance heuristic
        distance = 0
        for i in range(1, 9):
            current_index = state.index(i)
            goal_index = self.goal_index(i)
            distance += abs(current_index // 3 - goal_index // 3) + abs(current_index % 3 - goal_index % 3)
        return distance

    def goal_index(self, value):
        return value - 1

    def neighbors(self, state):
        blank_index = state.index(0)
        row, col = divmod(blank_index, 3)
        possible_moves = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        valid_moves = [(r, c) for r, c in possible_moves if 0 <= r < 3 and 0 <= c < 3]
        neighbors = [self.make_move(state, row, col, r, c) for r, c in valid_moves]
        return neighbors

    def make_move(self, state, from_row, from_col, to_row, to_col):
        new_state = state.copy()
        from_index = from_row * 3 + from_col
        to_index = to_row * 3 + to_col
        new_state[from_index], new_state[to_index] = new_state[to_index], new_state[from_index]
        return new_state

    def generate_random_state(self):
        random.shuffle(self.initial_state)
        self.current_state = self.initial_state
        self.update_gui()

    def update_gui(self):
        puzzle_text.set('\n'.join([str(row) for row in chunks(self.current_state, 3)]))


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def bfs_handler():
    puzzle.solve_bfs()


def dfs_handler():
    puzzle.solve_dfs()


def a_star_handler():
    puzzle.solve_a_star()


def random_handler():
    puzzle.generate_random_state()


# Create the main window
root = tk.Tk()
root.title("8-Puzzle Solver")

# Create puzzle object with an initial state
initial_state = [1, 2, 5, 3, 4, 0, 6, 7, 8]
puzzle = EightPuzzle(initial_state)

# Create and place puzzle text
puzzle_text = tk.StringVar()
puzzle_label = tk.Label(root, textvariable=puzzle_text, font=("Helvetica", 12), justify=tk.LEFT)
puzzle_label.grid(row=0, column=0, columnspan=3)

# Create buttons for BFS, DFS, A* and Random
bfs_button = tk.Button(root, text="BFS", command=bfs_handler)
bfs_button.grid(row=1, column=0)

dfs_button = tk.Button(root, text="DFS", command=dfs_handler)
dfs_button.grid(row=1, column=1)

a_star_button = tk.Button(root, text="A*", command=a_star_handler)
a_star_button.grid(row=1, column=2)

random_button = tk.Button(root, text="Random", command=random_handler)
random_button.grid(row=2, column=1)

# Run the Tkinter event loop
root.mainloop()
