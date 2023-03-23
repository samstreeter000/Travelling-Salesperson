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

def city_printer(final_route):
    city_path=list()
    for index in final_route:
        city_path.append(cities[index])
    return city_path

def tsp_greedy():
    city_index = list()
    for i in range(len(cities)):
        city_index.append(i)
    paths=list()
    for start_city in city_index:
        route=[start_city]
        new_cities=city_index.copy()
        new_cities.remove(start_city)
        while new_cities!=[]:
            shortest_step=1000
            for city in new_cities:
                step=distance_finder(route[-1],city)
                if step<shortest_step:
                    shortest_step=step
                    next_city=city
            route.append(next_city)
            new_cities.remove(next_city)
        paths.append((route,route_distance_finder(route)))
        length=10000
        for tuple in paths:
            if tuple[1]<length:
                length=tuple[1]
                final_route=tuple
    return final_route

print(tsp_greedy())