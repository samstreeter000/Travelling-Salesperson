##These four functions appears in all three algorithims, they serve to open files, compute distance between cities
##and over routes and convert lists of city indexes to the names of the cities.
def file_opener(name_file,distance_file):
    """

    :param name_file: The text file containing the names
    of the cities
    :param distance_file: The text file containing the
    distances between all city pairs
    :return: None. This function creates global
    lists cities and distance.
    """
    try:
        distances = open(distance_file)
        names = open(name_file)
    except:
        print('Cannot open input file.')
    global cities
    cities = list()
    #creates the list cities by reading the names text file
    for line in names:
        cities.append(line.strip('\n'))
    global distance
    distance = list()
    #creates the list distance by reading the names text file
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
    :return: The distance covered by following the route
    and returning to the initial city
    """
    travel = 0
    for i in range(0, len(route)):
        ## If i is the final entry in route, we find the
        ##distance between it and the final entry
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
    :param final_route:
    :return:
    """
    city_path=list()
    for index in final_route:
        city_path.append(cities[index])
    return city_path

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
    ##recusriv function.
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