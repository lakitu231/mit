###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    
    cow_dict = {}
    
    with open(filename) as f:
        for line in f:
            pair = line.split(',')
            cow_dict[pair[0]] = int(pair[1])

    return cow_dict
    

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    # Make copy of cows as a sorted dict by value
    cows_left = {k: v for k, v in sorted(cows.items(), key=lambda item: item[1], reverse=True)}
    
    trips = []
    
    while cows_left != {}:
        
        # For each trip
        free_space = limit
        current_trip = []
        
        for name, weight in cows_left.items():
            if weight <= free_space:
                free_space -= weight
                current_trip.append(name)
            
        for name in current_trip:
            del cows_left[name]
                
        trips.append(current_trip)
        
    return(trips)


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
        
    alts = []
    for trips in get_partitions(cows.keys()):
        within_limit = True
        
        for trip in trips:
            if sum(cows[name] for name in trip) > limit:
                within_limit = False
                break
        
        if within_limit:
            alts.append(trips)
        
    return sorted(alts, key=len)[0]

    # ======
    # SLOWER
    # trips = []
    # for partition in get_partitions(cows.keys()):
    #     trips.append(partition)
    
    # for trips in sorted(trips, key = len):
    #     within_limit = True
        
    #     for trip in trips:
    #         if sum(cows[name] for name in trip) > limit:
    #             within_limit = False
    #             break
        
    #     if within_limit:
    #         return(trips)
        
    
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    
    # Greedy Cow Transport
    print("Greedy Cow Transport")

    start = time.time()
    greedy_trips = greedy_cow_transport(cows)
    end = time.time()
    
    # i = 1
    # for trip in greedy_trips:
    #     print(f'trip {i}: {trip}')
    #     i += 1
    
    print(f'Number of trips : {len(greedy_trips)}')    
    print(f'Time taken to run : {end - start:.3f} seconds')    

    # Brute Force Cow Transport
    print("\nBrute Force Cow Transport")

    start = time.time()
    brute_trips = brute_force_cow_transport(cows)
    end = time.time()
    
    # i = 1
    # for trip in brute_trips:
    #     print(f'trip {i}: {trip}')
    #     i += 1
    
    print(f'Number of trips : {len(brute_trips)}')    
    print(f'Time taken to run : {end - start:.3f} seconds')   


if __name__ == '__main__':
    cows = load_cows('ps1_cow_data.txt')
    compare_cow_transport_algorithms()
