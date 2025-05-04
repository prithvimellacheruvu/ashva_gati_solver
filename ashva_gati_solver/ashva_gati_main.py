from ashva_gati_library import KnightsTour, TourManager

# === Example usage ===
if __name__ == "__main__":
    master_tour = KnightsTour.from_file("master_solution.txt")
    manager = TourManager(master_tour)
    magic_tours = manager.get_magic_squares()

    print(f"Number of tours derived : {len(manager.all_tours)}")      

    print(f"Found {len(magic_tours)} magic knight's tours.")
    for idx, tour in magic_tours:
        print(f"Magic tour #{idx}")
        print(f"The magic number: {tour.magic_number}")