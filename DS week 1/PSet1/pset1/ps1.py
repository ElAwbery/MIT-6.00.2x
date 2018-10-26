###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

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

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


'''
# Problem 1

One way of transporting cows is to always pick the heaviest cow that will fit onto the spaceship first. 
This is an example of a greedy algorithm. So if there are only 2 tons of free space on your spaceship, 
with one cow that's 3 tons and another that's 1 ton, the 1 ton cow will get put onto the spaceship.

Implement a greedy algorithm for transporting the cows back across space in the function 
greedy_cow_transport. The function returns a list of lists, where each inner list represents a trip 
and contains the names of cows taken on that trip.

Note: Make sure not to mutate the dictionary of cows that is passed in!

Assumptions:

 - The order of the list of trips does not matter. That is, [[1,2],[3,4]] and [[3,4],[1,2]] are considered 
equivalent lists of trips.
 - All the cows are between 0 and 100 tons in weight.
 - All the cows have unique names.
 - If multiple cows weigh the same amount, break ties arbitrarily.
 - The spaceship has a cargo weight limit (in tons), which is passed into the function as a parameter.

Example:

Suppose the spaceship has a weight limit of 10 tons and the set of cows to transport is 
{"Jesse": 6, "Maybel": 3, "Callie": 2, "Maggie": 5}.

The greedy algorithm will first pick Jesse as the heaviest cow for the first trip. 
There is still space for 4 tons on the trip. Since Maggie will not fit on this trip, the greedy algorithm 
picks Maybel, the heaviest cow that will still fit. 
Now there is only 1 ton of space left, and none of the cows can fit in that space, so the first trip is 
[Jesse, Maybel].

For the second trip, the greedy algorithm first picks Maggie as the heaviest remaining cow, 
and then picks Callie as the last cow. Since they will both fit, this makes the second trip 
[[Maggie], [Callie]].

The final result then is [["Jesse", "Maybel"], ["Maggie", "Callie"]].
'''


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
    
    
    all_trips = []
    next_trip = []
    next_trip_weight = 0
    
    remaining = cows.copy()
    
    while len(remaining) > 0: 
        heaviest_by_name = sorted(remaining, key = remaining.__getitem__, reverse = True)
        
        for name in heaviest_by_name: # iterate through all remaining cows, add by heaviest fit first
            
            if next_trip_weight + remaining[name] <= limit:
                next_trip.append(name) # add cow name to next trip list
                next_trip_weight += remaining[name] # increment the weight
                del(remaining[name])  # remove cow from remaining
            
            if next_trip_weight == limit: # don't waste time checking cows if this trip is full
                break
            
            if next_trip_weight > limit:
                raise ValueError ("ship will crash, weight exceeded, abort packing process")
                
        all_trips.append(next_trip)
        next_trip = []
        next_trip_weight = 0
    
    return all_trips

cows = load_cows("ps1_cow_data.txt")
# tests
print("final greedy cows = ", greedy_cow_transport(cows, limit = 10))
                
'''
Another way to transport the cows is to look at every possible combination of trips and pick the best one. 
This is an example of a brute force algorithm. 
Implement a brute force algorithm to find the minimum number of trips needed to take all the cows across 
the universe in the function brute_force_cow_transport. 
The function returns a list of lists, where each inner list represents a trip and contains the 
names of cows taken on that trip.

Notes:

Make sure not to mutate the dictionary of cows!
In order to enumerate all possible combinations of trips, you will want to work with set partitions. 
We have provided you with a helper function called get_partitions that generates all the set partitions 
for a set of cows. More details on this function are provided below.

Assumptions:

 - Assume that order doesn't matter. (1) [[1,2],[3,4]] and [[3,4],[1,2]] are considered equivalent 
lists of trips. 
(2) [[1,2],[3,4]] and [[2,1],[3,4]] are considered the same partitions of [1,2,3,4].
 - You can assume that all the cows are between 0 and 100 tons in weight.
 - All the cows have unique names.
 - If multiple cows weigh the same amount, break ties arbitrarily.
 - The spaceship has a cargo weight limit (in tons), which is passed into the function as a parameter.


Example: 
    
Suppose the spaceship has a cargo weight limit of 10 tons and the set of cows to transport is 
{"Jesse": 6, "Maybel": 3, "Callie": 2, "Maggie": 5}.
The brute force algorithm will first try to fit them on only one trip, 
["Jesse", "Maybel", "Callie", "Maggie"]. Since this trip contains 16 tons of cows, it is over the weight 
limit and does not work. Then the algorithm will try fitting them on all combinations of two trips. 
Suppose it first tries [["Jesse", "Maggie"], ["Maybel", "Callie"]]. This solution will be rejected because 
Jesse and Maggie together are over the weight limit and cannot be on the same trip. 
The algorithm will continue trying two trip partitions until it finds one that works, such as 
[["Jesse", "Callie"], ["Maybel", "Maggie"]].
The final result is then [["Jesse", "Callie"], ["Maybel", "Maggie"]]. Note that depending on which cow 
it tries first, the algorithm may find a different, optimal solution. 
Another optimal result could be [["Jesse", "Maybel"],["Callie", "Maggie"]].    
'''

# Problem 2
def brute_force_cow_transport(cows,limit=10):
    
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
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
    best_yet = None
    
    for partition in get_partitions(cows):
        
        if within_weight_limit(cows, partition, limit):
            
            if (best_yet == None) or len(partition) < len(best_yet): 
                best_yet = partition
                    
    return best_yet
        
def within_weight_limit(cows, partition, limit):
    for cow_set in partition:
        cow_set_weight = 0
        for cow in cow_set:
            cow_weight = cows[cow]
            cow_set_weight += cow_weight
        
        if cow_set_weight > limit:
            return False
        
    return True
    
    
    
# test
cows = load_cows("ps1_cow_data.txt")

brute_force_cow_transport(cows, limit = 10)





'''
You can measure the time a block of code takes to execute using the time.time() function as follows. 
This prints the duration in seconds, as a float. For a very small fraction of a second, it will print 0.0.

start = time.time()
## code to be timed
end = time.time()
print(end - start)

Using the given default weight limits of 10 and the given cow data, both algorithms should not take 
more than a few seconds to run.
'''
       
# Problem 3
cows = load_cows("ps1_cow_data.txt")
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
    start = time.time()
    
    def greedy_cow_transport(cows,limit=10):
        """
        I/O as defined in function above
        """
    
        all_trips = []
        next_trip = []
        next_trip_weight = 0
        
        remaining = cows.copy()
        
        while len(remaining) > 0: 
            heaviest_by_name = sorted(remaining, key = remaining.__getitem__, reverse = True)
            
            for name in heaviest_by_name: # iterate through all remaining cows, add by heaviest fit first
                
                if next_trip_weight + remaining[name] <= limit:
                    next_trip.append(name) # add cow name to next trip list
                    next_trip_weight += remaining[name] # increment the weight
                    del(remaining[name])  # remove cow from remaining
                
                if next_trip_weight == limit: # don't waste time checking cows if this trip is full
                    break
                
                if next_trip_weight > limit:
                    raise ValueError ("ship will crash, weight exceeded, abort packing process")
                    
            all_trips.append(next_trip)
            next_trip = []
            next_trip_weight = 0
            
        
        return all_trips
    
    end = time.time()
    print("number of trips returned by Greedy Cow =", len(greedy_cow_transport(cows, limit = 10)))
    print("Greedy Cow run time = ", end - start)
    
    start2 = time.time()
    
    def brute_force_cow_transport(cows,limit=10):
        """
        I/O as defined in program above
        """
        best_yet = None
        
        for partition in get_partitions(cows):
            
            if within_weight_limit(cows, partition, limit):
                
                if (best_yet == None) or len(partition) < len(best_yet): 
                    best_yet = partition
                    
        
               
        return best_yet
            
    def within_weight_limit(cows, partition, limit):
        for cow_set in partition:
            cow_set_weight = 0
            for cow in cow_set:
                cow_weight = cows[cow]
                cow_set_weight += cow_weight
            
            if cow_set_weight > limit:
                return False
            
        return True
    
    end2 = time.time()
    print("Brute Force Cow run time =", end2 - start2)
    print ("number of trips returned by Brute Force Cow =", len(brute_force_cow_transport(cows, limit = 10)))
    
'''
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
'''

cows = load_cows("ps1_cow_data.txt")
limit=100
print(cows)

print(greedy_cow_transport(cows, limit))
print(brute_force_cow_transport(cows, limit))


