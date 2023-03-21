#ahhhhhhhhhhhhhhhhhhhhhhh
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
    between=float(distance[city_1][city_2])
    return between


def route_distance_finder(route):
    travel=0
    for i in range(0,len(route)):
        if i==len(route)-1:
            j=0
        else:
            j=i+1
        travel+=distance_finder(route[i],route[j])
    return travel



def mutator(initial_route):
    route=initial_route.copy()
    random1=-1
    random2=-1
    while random1==random2:
        random1 = random.randint(0,len(cities)-1)
        random2 = random.randint(0, len(cities) - 1)

    route.remove(random1)
    route.remove(random2)
    route.append(random1)
    route.append(random2)

    travelling=route_distance_finder(route)
    return route,travelling

def tsp_mutation():
    initial_route=list()
    travel_time=0
    for i in range(len(cities)):
        initial_route.append(i)
    initial_travel_time=route_distance_finder(initial_route)

    print(initial_route, initial_travel_time)
    print(mutator(initial_route))



print(tsp_mutation())