import numpy as np

class KnightsTour:
    def __init__(self, board):
        self.board = np.array(board)
        assert self.board.shape == (12, 12), "Board must be 12x12"

    @staticmethod
    def from_file(filepath):
        with open(filepath, 'r') as file:
            lines = file.readlines()
        board = [list(map(int, line.strip().split())) for line in lines]
        return KnightsTour(board)

    def shift_solution(self, offset):
        """Shift solution by changing start number by offset (modulo 144)"""
        shifted = (self.board + offset - 1) % 144 + 1
        return KnightsTour(shifted)

    def reverse_solution(self):
        """Reverse knight tour solution: 1 becomes 144, 2 becomes 143, etc."""
        reversed_board = 145 - self.board
        return KnightsTour(reversed_board)

    def is_magic_square(self, subgrid_size=4):
        """
        Checks if the board is a magic square:
        - All rows and columns sum to same value. Mandatory condition.
        - All non-overlapping subgrids of size subgrid_size x subgrid_size sum to same value. Internally assigned to a boolean is_subgrid_magic.
        """
        subgrid = self.board[0:subgrid_size, 0:subgrid_size]
        
        self.magic_number = np.sum(self.board[0])
        self.subgrid_magic_number = np.sum(subgrid)

        # Check rows
        for row in self.board:
            if np.sum(row) != self.magic_number:
                return False

        # Check columns
        for col in self.board.T:
            if np.sum(col) != self.magic_number:
                return False

        # Check subgrids (non-overlapping)
        self.is_subgrid_magic = True
        for i in range(0, 12, subgrid_size):
            for j in range(0, 12, subgrid_size):
                subgrid = self.board[i:i+subgrid_size, j:j+subgrid_size]
                if np.sum(subgrid) != self.subgrid_magic_number:
                    self.is_subgrid_magic = False
                    self.subgrid_magic_number = 0

        return True


class TourManager:
    def __init__(self, master_tour):
        self.master_tour = master_tour
        self.filename_all_tours = "solved_all_tours.txt"
        self.filename_magic_tours = "solved_magic_tours.txt"

    def generate_all_tours(self):
        """
        Generate all 288 knight tour solutions (original + shifts + reversed)
        """
        tours = []
        for offset in range(144):
            tour = self.master_tour.shift_solution(offset)
            tours.append(tour)
            tours.append(tour.reverse_solution())
        self.all_tours = tours

    def get_magic_squares(self):
        magic_squares = []
        self.generate_all_tours()
        for i, tour in enumerate(self.all_tours):
            if tour.is_magic_square():
                magic_squares.append((i, tour))        
        self.magic_squares = magic_squares
        return magic_squares
    
    def write_all_solutions(self):
        with open(self.filename_all_tours, 'w') as f:
            for idx, solution in enumerate(self.all_tours):
                f.write(f"# Solution {idx+1}\n")
                for row in solution.board:
                    f.write(" ".join(f"{val:3}" for val in row) + "\n")
                f.write("\n")
                
    def write_magic_solutions(self):
        with open(self.filename_magic_tours, 'w') as f:
            for idx, solution in self.magic_squares:
                f.write(f"# Magic Solution {idx+1} | Magic Sum = {solution.magic_number}")
                if solution.is_subgrid_magic:
                    f.write(f" | Subgrid Magic Sum = {solution.subgrid_magic_number}\n")
                else:
                    f.write(f"\n")
                
                for row in solution.board:
                    f.write(" ".join(f"{val:3}" for val in row) + "\n")
                f.write("\n")

