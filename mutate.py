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



def city_printer(final_route):
    city_path=list()
    for index in final_route:
        city_path.append(cities[index])
    return city_path


def mutator(previous_champion):
    """
    :param previous_champion: The parent route between cities to be mutated upon.
    :return: route,route_distance: a tuple containing the mutated route and the distance covering it.
    """
    ## The initial route is copied as to not disturb to the parent route when making multiple offspring.
    route=previous_champion.copy()
    ##Start 2 random number off at some arbitrary equivalent value and generate random numbers corresponding
    ## to city indexes until two distinct indexes are created
    random1=-1
    random2=-1
    random3=1
    while random1==random2: # or random1==random3 or random2==random3:
        random1 = random.randint(0,len(cities)-1)
        random2 = random.randint(0, len(cities)- 1)
        #random3 = random.randint(0, len(cities)- 1)
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

    #route.remove(random1)
    #route.remove(random2)
    #route.remove(random3)
    #route.append(random1)
    #route.append(random2)
    #route.append(random3)
    route_distance=route_distance_finder(route)
    return route,route_distance

def tsp_mutation(name_file,distance_file):
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
    file_opener(name_file,distance_file)
    ##The "previous champion" serves as the fittest individual and becomes the parent of preceeding generations.
    ## It becomes of the cities listed in order by their indices.
    previous_champion=list()
    for i in range(len(cities)):
        previous_champion.append(i)
    previous_champion_distance=route_distance_finder(previous_champion)
    ##Stagnations is the number of times mutating a parent fails to provide any superior offspring.
    ##Generations tracks the number of times offspring have been generated off a parent.
    stagnations=0
    generations=0
    ##Perfect parent is the best result produced by the whole algorithim, it is started as an arbitrarily bad route.
    perfect_parent=(list(),1000000)
    ##This while loop runs until 5 generations fail to produce offspring superior to their parent.
    while stagnations<5:
        ##Start a generation off with 0 offspring and an arbitraily bad "champion" to beat.
        offspring=0
        generation_champion = list()
        generation_champion_distance = 10000
        generations+=1
        ##This optional block of codeshuts the code down if 500 generations are ever created before 5 stagnations occur.
        ##if generations==500:
            ##print(previous_champion_distance)
            ##stagnations=5

        ##Create 2000 offspring using the mutator function. If any offspring is better than the
        ## previous champion within the generation, make it the new champion.
        while offspring<1000:
            new_route=mutator(previous_champion)
            if new_route[1]<generation_champion_distance:
                generation_champion=new_route[0]
                generation_champion_distance=new_route[1]
            offspring+=1
        ##After the best of a generation is found, it is compared to its parent, this first if branch handles the case
        ## where it is worse than its parent.
        if generation_champion_distance>previous_champion_distance:
            stagnations+=1
            ##Increments the number of stagnations and checks to see if our local minima is smaller than
            ## all previous local minima, storing it in perfect parent if so.
            if previous_champion_distance<perfect_parent[1]:
                perfect_parent=(previous_champion,previous_champion_distance)
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
    final_route=city_printer(perfect_parent[0])
    final_route_distance=perfect_parent[1]
            
    return generations,final_route,final_route_distance

##This line generates a evolutionary determined path between 30 cities in the relevant text files.
##The found solution varies, usually ranges from 500-550 for distance. It takes several seconds to resolve.
print(tsp_mutation("thirty_cities_names.txt","thirty_cities_dist.txt"))

