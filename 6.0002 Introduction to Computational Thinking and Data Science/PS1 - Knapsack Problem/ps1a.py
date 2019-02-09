###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: Anthony Lem
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time
import copy

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
    #Create a dictionary for the cows
    cows = {}
    #Open the file and add all cows and their weights to the dictionary
    with open(filename) as file: #Assumed to be opened as "r" = reading; use with to ensure the file closes properly
        for line in file:
            cow = line.split(",")
            cows[cow[0]] = int(cow[1]) #We have to use int here to cast the value as an integer, otherwise it will be a string with "\n" at the end of it.
    return cows

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
    trips = []
    copy_cows = copy.deepcopy(cows)
    weight = 0
    transported_cow = ""
    heaviest_cow = 0
    trip = []
    while len(copy_cows) > 0:
        #Select the heaviest cow
        for cow in cows:
            if cows[cow] + weight <= limit and cows[cow] > heaviest_cow and cow in copy_cows:
                transported_cow = cow
                heaviest_cow = cows[cow]
        #Take the heaviest cow
        #If the cow can fit on the trip take it
        if transported_cow != "":
            del copy_cows[transported_cow]
            trip.append(transported_cow)
            heaviest_cow = 0
            weight += cows[transported_cow]
            transported_cow = ""
        #Otherwise, move on to the next trip
        else:
            weight = 0
            trips.append(trip)
            trip = []
    return trips

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
    potential_solutions = {}
    for partition in get_partitions(cows):
        solution = True
        #print(partition)
        for L in partition:
            total_weight = 0
            for cow in L:
                total_weight += cows[cow]
            if total_weight > limit:
                solution = False
        if solution:
            number_of_trips = len(partition)
            potential_solutions[number_of_trips] = partition
    solution = min(potential_solutions.keys())
    return(potential_solutions[solution])
        
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
    cows = load_cows("ps1_cow_data.txt")
    start = time.time()
    ##code to be timed
    greedy_cow = greedy_cow_transport(cows)
    end = time.time()
    greedy_time = end - start
    start = time.time()
    brute_cow = brute_force_cow_transport(cows)
    end = time.time()
    brute_time = end - start
    print(len(greedy_cow), greedy_time, len(brute_cow), brute_time)

compare_cow_transport_algorithms()
