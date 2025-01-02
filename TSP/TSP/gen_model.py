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

    def __order_crossover(self, pcross):
        parent1, parent2 = self.__roulette_wheel_parent_selection()

        if not flip(pcross):
            return parent1, parent2

        jcross1 = rnd(0, len(parent1) - 2)
        jcross2 = rnd(jcross1 + 1, len(parent1) - 1)
        
        section1 = parent1[jcross1:jcross2]
        section2 = parent2[jcross1:jcross2]
        
        remaining1 = [city for city in parent2 if city not in section1]
        remaining2 = [city for city in parent1 if city not in section2]
        
        child1_cities = remaining1[:jcross1] + section1 + remaining1[jcross1:]
        child2_cities = remaining2[:jcross1] + section2 + remaining2[jcross1:]
        
        return Route(child1_cities), Route(child2_cities)

    def __roulette_wheel_parent_selection(self):
        total_fitness = sum(route.fitness for route in self.routes)
        probabilities = [route.fitness / total_fitness for route in self.routes]
        return random.choices(self.routes, weights=probabilities, k=2)