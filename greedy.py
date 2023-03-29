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
print(tsp_greedy("seven_cities_names.txt",'seven_cities_dist.txt'))
##This line generates a greedy path between 30 cities in the relevant text files.
##This solution has a distance of 527.0.
print(tsp_greedy("thirty_cities_names.txt","thirty_cities_dist.txt"))