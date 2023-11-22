import cProfile
import pstats

if __name__ == "__main__":
    # cProfile.run("main()", filename="profile_stats")

    # Load the profiling statistics
    stats = pstats.Stats("profile_stats")

    # Strip out all the directory names and show only the function names
    stats.strip_dirs()

    # Sort the statistics by cumulative time
    stats.sort_stats('cumulative')

    # Print the statistics for functions from the rlcard package
    # stats.print_stats("rlcard")

    rlcard_functions = [func for func in stats.stats if "rlcard" in func[0]]
    for func in rlcard_functions:
        stats.stats[func].print_stats()

    # Optionally, you can print total time spent in rlcard functions
    total_time_in_rlcard = sum(stats.stats[func].stats[('cumulative',)] for func in rlcard_functions)
    print(f"Total time spent in rlcard functions: {total_time_in_rlcard:.3f} seconds")