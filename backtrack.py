def file_opener(name_file,distance_file):
    try:
        distances = open(distance_file)
        names = open(name_file)
    except:
        print('Cannot open input file.')
    global cities
    cities = list()
    for line in names:
        cities.append(line.strip('\n'))
    global distance
    distance = list()
    for line in distances:
        length = line.split()
        distance.append(length)

    return cities, distance


file_opener("seven_cities_names.txt",'seven_cities_dist.txt')


def distance_finder(city_1,city_2):
    between = float(distance[city_1][city_2])
    return between


def route_distance_finder(route):
    travel = 0
    for i in range(0, len(route)):
        if i == len(route)-1:
            j = 0
        else:
            j = i+1
        travel += distance_finder(route[i], route[j])
    return travel


all_routes = list()


def tsp_backtrack():
    initial_route = list()
    for i in range(len(cities)):
        initial_route.append(i)
    initial_travel_time = route_distance_finder(initial_route)
    print(initial_route)
    return initial_travel_time



print(tsp_backtrack())
