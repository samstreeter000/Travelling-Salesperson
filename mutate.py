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

##print(file_opener("seven_cities_names.txt",'seven_cities_dist.txt'))
##print(file_opener("thirty_cities_names.txt","thirty_cities_dist.txt"))

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

##print(route_distance_finder([0,3,5,6,1,2,4,29,27,12,13,15]))

def city_printer(final_route):
    city_path=list()
    for index in final_route:
        city_path.append(cities[index])
    return city_path


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
    for i in range(len(cities)):
        initial_route.append(i)
    initial_travel_time=route_distance_finder(initial_route)
    STOP = 0
    previous_champion = 10000
    while STOP<100:
        gen=list()
        offspring=0
        while offspring<100:
            new_route=mutator(initial_route)
            gen.append(new_route)
            offspring+=1
        highest_fitness=10000
        for tuple in gen:
            if int(tuple[1])<highest_fitness:
                highest_fitness=int(tuple[1])
                saved_tuple=tuple
        previous_champion=saved_tuple[1]
        initial_route=saved_tuple[0]
        STOP+=1
    final_route=city_printer(saved_tuple[0])
    return final_route,previous_champion

##file_opener("seven_cities_names.txt",'seven_cities_dist.txt')
##print(tsp_mutation())
file_opener("thirty_cities_names.txt","thirty_cities_dist.txt")
print(tsp_mutation())

