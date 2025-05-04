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

    def is_magic_square(self, subgrid_size=3):
        """
        Checks if the board is a magic square:
        - All rows and columns sum to same value
        - All non-overlapping subgrids of size subgrid_size x subgrid_size sum to same value
        """
        target_sum = np.sum(self.board[0])

        # Check rows
        for row in self.board:
            if np.sum(row) != target_sum:
                return False

        # Check columns
        for col in self.board.T:
            if np.sum(col) != target_sum:
                return False

        # Check subgrids (non-overlapping)
        for i in range(0, 12, subgrid_size):
            for j in range(0, 12, subgrid_size):
                subgrid = self.board[i:i+subgrid_size, j:j+subgrid_size]
                if np.sum(subgrid) != target_sum:
                    return False

        return True


class TourManager:
    def __init__(self, master_tour):
        self.master_tour = master_tour

    def generate_all_tours(self):
        """
        Generate all 288 knight tour solutions (original + shifts + reversed)
        """
        tours = []
        for offset in range(144):
            tour = self.master_tour.shift_solution(offset)
            tours.append(tour)
            tours.append(tour.reverse_solution())
        return tours

    def get_magic_squares(self):
        magic_squares = []
        all_tours = self.generate_all_tours()
        for i, tour in enumerate(all_tours):
            if tour.is_magic_square():
                magic_squares.append((i, tour))
        return magic_squares


# === Example usage ===
if __name__ == "__main__":
    master_tour = KnightsTour.from_file("master_solution.txt")
    manager = TourManager(master_tour)
    magic_tours = manager.get_magic_squares()

    print(f"Found {len(magic_tours)} magic knight's tours.")
    for idx, tour in magic_tours:
        print(f"Magic tour #{idx}")
