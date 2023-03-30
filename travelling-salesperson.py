import random
##These four functions appears in all three algorithims, they serve to open files, compute distance between cities
##and over routes and convert lists of city indexes to the names of the cities.
def file_opener(name_file,distance_file):
    """
    :param name_file: The text file containing the names
    of the cities
    :param distance_file: The text file containing the
    distances between all city pairs
    :return: None. This function creates global
    lists cities and distance that will be refrenced to later
    """
    try:
        distances = open(distance_file)
        names = open(name_file)
    except:
        print('Cannot open input file.')
    global cities
    cities = list()
    #creates the global list cities by reading the names text file
    for line in names:
        cities.append(line.strip('\n'))
    global distance
    distance = list()
    #creates the global list distance by reading the names text file
    for line in distances:
        length = line.split()
        distance.append(length)
def distance_finder(city_1,city_2):
    """
    :param city_1: The index of the first city
    :param city_2: The index of the second city
    :return: The distance between the two cities
    """
    #Uses the list distance to find the distance
    #between any two given cities
    between = float(distance[city_1][city_2])
    return between
def route_distance_finder(route):
    """
    :param route: A list of city indices detailing the
    order the cities were visited in.
    :return: travel: The distance covered by following the route
    and returning to the starting city
    """
    travel = 0
    for i in range(0, len(route)):
        ## If i is the final entry in route, we find the
        ##distance between it and the first entry
        if i == len(route)-1:
            j = 0
        else:
            j = i+1
            #here we use distance_finder to find the distance
            #between two subsequent cities in the route.
        travel += distance_finder(route[i], route[j])
    return travel
def city_printer(final_route):
    """
    :param final_route: A list of city indices detailing the
    order the cities were visited in.
    :return:city_path: A list of city names detailing the
    order the cities were visited in.
    """
    city_path=list()
    ##This for loop uses the index of a city and translates it to
    ## the city name and compiles these city names into a list that
    ## details the order cities were visited in.
    for index in final_route:
        city_path.append(cities[index])
    return city_path

##########################

##Begin the backtracking algorithim.
def tsp_backtrack(name_file,distance_file):
    """
    :param name_file: The text file containing the names
    of the cities
    :param distance_file: The text file containing the
    distances between all city pairs
    :return:path: The list of city names in the order they were visited in the optimized path.
    :return:best[1]: The length of the distance travelled over the optimal path.
    """
    global best_route_distance
    global best_route
    ## The best_route is initialized as an empty list with an arbitrarily large distance, so that any proposed path will be shorter in distance.
    best_route_distance = 1000
    best_route = list()
    ## Opens the relevant files and creates global lists cities and distance.
    file_opener(name_file,distance_file)
    ## This for loop initializes the list of remaning cities to consider, it includes all the indexes of the relevant cities, excluding city index 0,
    ## as that city will always be our starting point.
    remaining_cities=list()
    for index in range(1,len(cities)):
        remaining_cities.append(index)
    initial_route=[0]
    ## tsp_recursion returns the absolute best route over the search space as well as its distance as an ordered pair.
    best=tsp_recursion(initial_route,remaining_cities)
    ##city printer uses the list of city indexes in the best route and translates them to the names of city in the list
    path=city_printer(best[0])
    return path,best[1]

def tsp_recursion(initial_route,remaining_cities):
    """
    :param initial_route: This input is the partial route that is being built recursively.
    :param remaining_cities: The cities that are left to be visited for the current route being built.
    :return:
    """
    global best_route_distance
    global best_route
    ##If there are no more cities to be visited and the current route has a shorter distance covered than the previous best route,
    ##then store the current route as the best route.
    if remaining_cities==list():
        if route_distance_finder(initial_route)<best_route_distance:
            best_route_distance=route_distance_finder(initial_route)
            best_route=initial_route
    ##Otherwise, we need to continue building our path. If we have exactly one element in our current route, then we generate the second and final entries
    ##simultaneously, append them to our current route, remove them from remaining cities and feed the updated current route into our recursive function.
    ##Generating the second and list cities simultaneously keeps us from considering routes that are simply rotations of other routes.
    elif len(initial_route)==1:
        for city1 in remaining_cities:
            for city2 in remaining_cities:
                if city1<city2:
                    route=initial_route.copy()
                    locations=remaining_cities.copy()
                    route.append(city1)
                    route.append(city2)
                    locations.remove(city1)
                    locations.remove(city2)
                    tsp_recursion(route,locations)
    ##If our current route has more than one element, then we append a city, remove it from the remaining cities list and feed it into the
    ##recursive function.
    else:
        for city in remaining_cities:
            route = initial_route.copy()
            locations = remaining_cities.copy()
            route.insert(-1,city)
            locations.remove(city)
            tsp_recursion(route, locations)
    return best_route,best_route_distance

##This line generates the absolute shortest path between 7 cities in the relevant text files.
##This solution is:(['Alpha', 'Epsilon', 'Gamma', 'Delta', 'Zeta', 'Beta', 'Eta'], 106.4).
print(tsp_backtrack("seven_cities_names.txt",'seven_cities_dist.txt'))

##########################

##Begin the greedy algorithim.

def tsp_greedy(name_file,distance_file):
    """
    :param name_file: The text file containing the names
    of the cities
    :param distance_file: The text file containing the
    distances between all city pairs
    :return:best_route: The list of city names in the order they were visited in the optimized path.
    :return:best_route_distance: The length of the distance travelled over the optimal path.
    """
    ## Opens the relevant files and creates global lists cities and distance.
    file_opener(name_file,distance_file)
    ## This for loop generates a list of integers ranging from 0 to the
    ##number of cities minus one.
    city_index = list()
    for i in range(len(cities)):
        city_index.append(i)
    ##Initalzie best route as an empty list with an arbitrarily high corresponding distance.
    best_route=list()
    best_route_distance=100000
    ##We now use a for loop that will create one route for each city we have, starting each route with the corresponding city.
    for start_city in city_index:
        route=[start_city]
        remaining_cities=city_index.copy()
        remaining_cities.remove(start_city)
        ##This while loop looks at the current route being built and determines what city is closest to the final city in the
        ## route. That city is then removed from the list of available cities and the process is repeated
        ##until all the city options are exhausted.
        while remaining_cities!=[]:
            shortest_step=1000
            for city in remaining_cities:
                step=distance_finder(route[-1],city)
                if step<shortest_step:
                    shortest_step=step
                    next_city=city
            route.append(next_city)
            remaining_cities.remove(next_city)
            ##After an entire route has been generated, this if statement checks if that route
            ## is the best route found so far, that is starting at which city produces the best results
        if route_distance_finder(route)<best_route_distance:
            best_route_distance=route_distance_finder(route)
            ##City printer converts the current best route into a list of city names.
            best_route=city_printer(route)
    return best_route,best_route_distance


##This line generates a greedy path between 7 cities in the relevant text files.
##This solution is:(['Eta', 'Alpha', 'Epsilon', 'Gamma', 'Delta', 'Beta', 'Zeta'], 114.3).
##It is notably worse than the optimal path found by backtracking
##print(tsp_greedy("seven_cities_names.txt",'seven_cities_dist.txt'))
##This line generates a greedy path between 30 cities in the relevant text files.
##This solution has a distance of 527.0.
print(tsp_greedy("thirty_cities_names.txt","thirty_cities_dist.txt"))

##########################

##Begin the evolutionary algorithim.

def mutator(previous_champion):
    """
    :param previous_champion: The parent route between cities to be mutated upon.
    :return: route,route_distance: a tuple containing the mutated route and the distance covering it.
    """
    ## The initial route is copied as to not disturb to the parent route when making multiple offspring.
    route = previous_champion.copy()
    ##Start 2 random number off at some arbitrary equivalent value and generate random numbers corresponding
    ## to city indexes until two distinct indexes are created
    random1 = -1
    random2 = -1
    random3 = 1
    while random1 == random2:  # or random1==random3 or random2==random3:
        random1 = random.randint(0, len(cities) - 1)
        random2 = random.randint(0, len(cities) - 1)
        # random3 = random.randint(0, len(cities)- 1)
    ##Remove the randomly selected cities from the route and adds them on
    ## at random places in the route. The option to remove a third city is available

    route.remove(random1)
    route.remove(random2)
    ##route.remove(random3)
    index1 = random.randint(0, len(route) - 1)
    route.insert(index1, random1)
    index2 = random.randint(0, len(route) - 1)
    route.insert(index2, random2)
    ##index3 = random.randint(0, len(route) - 1)
    ##route.insert(index3, random3)

    ##Multiple mutation methods were tried, the following simply adds the random cities to the end of the list
    ## instead of randomly inserting them.

    # route.remove(random1)
    # route.remove(random2)
    # route.remove(random3)
    # route.append(random1)
    # route.append(random2)
    # route.append(random3)
    route_distance = route_distance_finder(route)
    return route, route_distance


def tsp_mutation(name_file, distance_file):
    """
    :param name_file: The text file containing the names
    of the cities
    :param distance_file: The text file containing the
    distances between all city pairs
    :return:generations:This variable counts how many times a generation of offspring were generated.
    :return:best_route: The list of city names in the order they were visited in the optimized path.
    :return:best_route_distance: The length of the distance travelled over the optimal path.
    """
    ## Opens the relevant files and creates global lists cities and distance.
    file_opener(name_file, distance_file)
    ##The "previous champion" serves as the fittest individual and becomes the parent of preceeding generations.
    ## It becomes of the cities listed in order by their indices.
    previous_champion = list()
    for i in range(len(cities)):
        previous_champion.append(i)
    previous_champion_distance = route_distance_finder(previous_champion)
    ##Stagnations is the number of times mutating a parent fails to provide any superior offspring.
    ##Generations tracks the number of times offspring have been generated off a parent.
    stagnations = 0
    generations = 0
    ##Perfect parent is the best result produced by the whole algorithim, it is started as an arbitrarily bad route.
    perfect_parent = (list(), 1000000)
    ##This while loop runs until 5 generations fail to produce offspring superior to their parent.
    while stagnations < 5:
        ##Start a generation off with 0 offspring and an arbitraily bad "champion" to beat.
        offspring = 0
        generation_champion = list()
        generation_champion_distance = 10000
        generations += 1
        ##This optional block of codeshuts the code down if 500 generations are ever created before 5 stagnations occur.
        ##if generations==500:
        ##print(previous_champion_distance)
        ##stagnations=5

        ##Create 2000 offspring using the mutator function. If any offspring is better than the
        ## previous champion within the generation, make it the new champion.
        while offspring < 1000:
            new_route = mutator(previous_champion)
            if new_route[1] < generation_champion_distance:
                generation_champion = new_route[0]
                generation_champion_distance = new_route[1]
            offspring += 1
        ##After the best of a generation is found, it is compared to its parent, this first if branch handles the case
        ## where it is worse than its parent.
        if generation_champion_distance > previous_champion_distance:
            stagnations += 1
            ##Increments the number of stagnations and checks to see if our local minima is smaller than
            ## all previous local minima, storing it in perfect parent if so.
            if previous_champion_distance < perfect_parent[1]:
                perfect_parent = (previous_champion, previous_champion_distance)
            ##Regardless, the previous champion is mutated thrice and set as the new parent.
            mutant1 = mutator(previous_champion)
            mutant2 = mutator(mutant1[0])
            mutant3 = mutator(mutant2[0])
            previous_champion = mutant3[0]
            previous_champion_distance = mutant3[1]

            ##If there is an offspring better than its parent, make it the new parent.
        else:
            previous_champion = generation_champion
            previous_champion_distance = generation_champion_distance
    ##After 5 stagnations occur, extract the list of city names and distance covering their
    ## route from perfect parent.
    final_route = city_printer(perfect_parent[0])
    final_route_distance = perfect_parent[1]

    return generations, final_route, final_route_distance


##This line generates a evolutionary determined path between 30 cities in the relevant text files.
##The found solution varies, usually ranges from 500-550 for distance. It takes several seconds to resolve.
print(tsp_mutation("thirty_cities_names.txt", "thirty_cities_dist.txt"))