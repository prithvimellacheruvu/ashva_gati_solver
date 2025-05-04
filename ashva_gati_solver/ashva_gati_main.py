from ashva_gati_library import KnightsTour, TourManager

if __name__ == "__main__":
    master_tour = KnightsTour.from_file("master_solution.txt")
    manager = TourManager(master_tour)
    magic_tours = manager.get_magic_squares()

    print(f"Number of tours derived : {len(manager.all_tours)}.")      

    print(f"Found {len(magic_tours)} magic knight's tours.")
    for idx, tour in magic_tours:
        print(f"Magic tour #{idx+1}")
        print(f"The magic number: {tour.magic_number}.")
        if tour.is_subgrid_magic:
            print(f"This is also a subgrid magic square. The subgrid magic number being: {tour.subgrid_magic_number}.")
            
    print(f"Exporting solutions.")
    manager.write_all_solutions()
    manager.write_magic_solutions()
    print(f"Done.")