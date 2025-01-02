import random
import numpy as np

def flip(probability):
    return random.random() < probability

def rnd(low, high):
    return random.randint(low, high)

class City: # Gene
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.__distances_to_other_cities = {}
    
    def distance_to(self, city):
        if city.name in self.__distances_to_other_cities:
            return self.__distances_to_other_cities[city.name]
        else:
            distance = np.sqrt((self.x - city.x) ** 2 + (self.y - city.y) ** 2)
            self.__distances_to_other_cities[city.name] = distance
            return distance

class Route: # Chromosome
    def __init__(self, cities):
        self.cities = cities
        self.n = len(cities)
        self.__travel_cost = 0
        self.__fitness = 0

    @property
    def fitness(self):
        if self.__fitness == 0:
            self.__fitness = 1 / self.travel_cost
        return self.__fitness

    @property
    def travel_cost(self):
        if self.__travel_cost == 0:
            path_cost = sum([self.cities[i].distance_to(self.cities[i+1]) for i in range(self.n-1)])
            path_cost += self.cities[-1].distance_to(self.cities[0])
            self.__travel_cost = path_cost
        return self.__travel_cost

    def mutate(self, pmutation):
        if flip(pmutation):
            i, j = random.sample(range(self.n), 2)
            self.__swap_cities(i, j)
            self.__reset_params()
    
    def __swap_cities(self, i, j):
        self.cities[i], self.cities[j] = self.cities[j], self.cities[i]
        
    def __reset_params(self):
        self.__travel_cost = 0
        self.__fitness = 0
        
    def __getitem__(self, index):
        return self.cities[index]
    
    def __len__(self):
        return self.n
    
    def __str__(self):
        return ' -> '.join(city.name for city in self.cities)

class Population:
    def __init__(self, routes):
        self.routes = routes
        self.n = len(routes)
        
    @staticmethod
    def initialize_population(cities, popsize):
        population = []
        for _ in range(popsize):
            route = Route(random.sample(cities, len(cities)))
            population.append(route)
        return population

    def reproduce(self, pmutation, pcross):
        new_population = []
        while len(new_population) < self.n:
            child1, child2 = self.__order_crossover(pcross)
            child1.mutate(pmutation)
            child2.mutate(pmutation)
            new_population.extend([child1, child2])
        self.routes = new_population[:self.n]
        
    def get_fitness(self):
        fitnesses = [route.fitness for route in self.routes]
        return (max(fitnesses), min(fitnesses), sum(fitnesses) / self.n)

    def get_travel_costs(self):
        travel_costs = [route.travel_cost for route in self.routes]
        return (max(travel_costs), min(travel_costs), sum(travel_costs) / self.n)


    # def __order_crossover(self, pcross):
        # parent1, parent2 = self.__roulette_wheel_parent_selection() #[9, 8, 4, 5, 6, 7, 1, 3, 2, 10], [8, 7, 1, 2, 3, 10, 9, 5, 4, 6]

        # if not flip(pcross):
        #     return parent1, parent2
        
        # jcross1 = rnd(1, len(parent1) - 2)
        # jcross2 = rnd(jcross1 + 1, len(parent1) - 1)

        # cross_len = jcross2 - jcross1
        
        # section1 = parent2[jcross1:jcross2]
        # section2 = parent1[jcross1:jcross2]

        # queue_end1 = []
        # queue_end2 = []

        # for i in range(jcross2, len(parent1)):
        #     if parent1[i] not in section1:
        #         queue_end1.append(parent1[i])
        #     if parent2[i] not in section2:
        #         queue_end2.append(parent2[i])
        
        # queue_begin1 = []
        # queue_begin2 = []
            
        # for i in range(jcross1):
        #     if parent1[i] not in section1:
        #         queue_begin1.append(parent1[i])
        #     if parent2[i] not in section2:
        #         queue_begin2.append(parent2[i])
        
        # remaining_begin1 = [x for x in section2 if x not in section1] + queue_begin1
        # remaining_begin2 = [x for x in section1 if x not in section2] + queue_begin2
        # child1_route = []
        # child2_route = []
        # section_iter = 0;
        # remaining1_iter = 0
        # remaining2_iter = 0
        # end1_iter = 0
        # end2_iter = 0

        # for i in range(len(parent1)):
        #     if i >= jcross1 and section_iter < cross_len:
        #         child1_route.append(section1[section_iter])
        #         child2_route.append(section2[section_iter])
        #         section_iter += 1
                
        #     elif i >= jcross2:
        #         if(end1_iter < len(queue_end1)):
        #             child1_route.append(queue_end1[end1_iter])
        #             end1_iter += 1
        #         else:
        #             child1_route.append(remaining_begin1[remaining1_iter])
        #             remaining1_iter += 1
                    
        #         if (end2_iter < len(queue_end2)):
        #             child2_route.append(queue_end2[end2_iter])
        #             end2_iter += 1
        #         else:
        #             child2_route.append(remaining_begin2[remaining2_iter])
        #             remaining2_iter +=1
        #     else:
        #         if(remaining1_iter < len(remaining_begin1)):
        #             child1_route.append(remaining_begin1[remaining1_iter])
        #             remaining1_iter += 1
        #         else:
        #             child1_route.append(queue_end1[end1_iter])
        #             end1_iter += 1
                
        #         if (remaining2_iter < len(remaining_begin2)):
        #             child2_route.append(remaining_begin2[remaining2_iter])
        #             remaining2_iter +=1
        #         else:
        #             child2_route.append(queue_end2[end2_iter])
        #             end2_iter += 1

        # child1 = Route(child1_route)
        # child2 = Route(child2_route)

        # return child1, child2

    def __order_crossover(self, pcross):
        parent1, parent2 = self.__roulette_wheel_parent_selection()

        if not flip(pcross):
            return parent1, parent2

        jcross1 = rnd(1, len(parent1) - 2)
        jcross2 = rnd(jcross1 + 1, len(parent1) - 1)
        
        section1 = parent1.cities[jcross1:jcross2]
        section2 = parent2.cities[jcross1:jcross2]
        
        remaining1 = [city for city in parent2.cities if city not in section1]
        remaining2 = [city for city in parent1.cities if city not in section2]
        
        child1_cities = remaining1[:jcross1] + section1 + remaining1[jcross1:]
        child2_cities = remaining2[:jcross1] + section2 + remaining2[jcross1:]
        
        return Route(child1_cities), Route(child2_cities)

    def __roulette_wheel_parent_selection(self):
        total_fitness = sum(route.fitness for route in self.routes)
        probabilities = [route.fitness / total_fitness for route in self.routes]
        return random.choices(self.routes, weights=probabilities, k=2)