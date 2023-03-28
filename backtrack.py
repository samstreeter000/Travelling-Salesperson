import random

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
    remaining_cities = [0, 1, 2, 3, 4, 5, 6]
    initial_route = list()
    for i in range(len(cities)):
        initial_route.append(i)
    initial_travel_time = route_distance_finder(initial_route)
    all_routes.append(initial_travel_time)

    for n in range(0, 361):
        new_route = list()
        for num in remaining_cities:
            new_route.append(num)
            remaining_cities.remove(num)
            for num1 in remaining_cities:
                if num1 < num:
                    remaining_cities.remove(num1)

        print(new_route)
        new_travel_time = route_distance_finder(new_route)
        if new_travel_time < initial_travel_time:
            all_routes.append(new_travel_time)

    return min(all_routes)


print(tsp_backtrack())
