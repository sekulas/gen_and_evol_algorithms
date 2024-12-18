import random
import numpy as np
import matplotlib.pyplot as plt

x_min = -1
x_max = 21
popsize = 20
generations = 50
lchrom = 5
pcross = 0.7
pmutation = 0.001

def function(x):
    return -0.5 * x ** 2 + 10 * x + 13

def fitness_function(x):
    result = function(x)
    return result if result > 0 else 0

def flip(probability):
    return random.random() < probability

def rnd(low, high):
    return random.randint(low, high)

def roulette_wheel_selection(population, fitness_sum):
    pick = random.random() * fitness_sum
    current = 0
    for chromosome, fitness in population:
        current += fitness
        if current > pick:
            return chromosome
    return population[-1][0]

def crossover(parent1, parent2, lchrom, pcross, pmutation):
    child1, child2 = parent1[:], parent2[:]
    
    if flip(pcross):  
        jcross = rnd(1, lchrom-1)
        child1 = parent1[:jcross] + parent2[jcross:]
        child2 = parent2[:jcross] + parent1[jcross:]

    return child1, child2

def mutate(chromosome, pmutation):
    for i in range(len(chromosome)):
        if flip(pmutation):
            chromosome[i] = 1 - chromosome[i]
    return chromosome

def decode(chromosome, x_min, x_max):
    binary_str = ''.join(map(str, chromosome))
    decimal_value = int(binary_str, 2)
    max_val = (2 ** len(chromosome)) - 1
    return round(x_min + (x_max - x_min) * decimal_value / max_val)

def initialize_population(popsize, lchrom, x_min, x_max):
    population = []
    for _ in range(popsize):
        chromosome = random.choices([0, 1], k=lchrom)
        decoded_value = decode(chromosome, x_min, x_max)
        population.append([chromosome, fitness_function(decoded_value)])
    return population

def genetic_algorithm(fitness_function, x_min, x_max, popsize, generations, lchrom, pcross, pmutation):
    population = initialize_population(popsize, lchrom, x_min, x_max)
    
    history = {
        "max_fitness": [],
        "min_fitness": [],
        "avg_fitness": []
    }
    
    for generation in range(generations):
        fitness_sum = 0
        for i in range(popsize):
            decoded_value = decode(population[i][0], x_min, x_max)
            fitness = fitness_function(decoded_value)
            population[i][1] = fitness
            fitness_sum += fitness
        
        
        fitness_values = [ind[1] for ind in population]
        history["max_fitness"].append(max(fitness_values))
        history["min_fitness"].append(min(fitness_values))
        history["avg_fitness"].append(sum(fitness_values) / popsize)
        
        new_population = []
        while len(new_population) < popsize:
            parent1 = roulette_wheel_selection(population, fitness_sum)
            parent2 = roulette_wheel_selection(population, fitness_sum)
            
            child1, child2 = crossover(parent1, parent2, lchrom, pcross, pmutation)
            
            child1 = mutate(child1, pmutation)
            child2 = mutate(child2, pmutation)
            
            new_population.extend([[child1, 0], [child2, 0]])
        
        population = new_population[:popsize]
    
    plot_results(history, x_min, x_max, fitness_function)

def plot_results(history, x_min, x_max, fitness_function):
    generations = range(len(history["max_fitness"]))
    
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(generations, history["max_fitness"], label="Max Fitness")
    plt.plot(generations, history["min_fitness"], label="Min Fitness")
    plt.plot(generations, history["avg_fitness"], label="Avg Fitness")
    plt.title("Evolution of Fitness")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend()
    
    plt.subplot(1, 2, 2)
    x_values = np.linspace(x_min, x_max, 100)
    y_values = [fitness_function(x) for x in x_values]
    plt.plot(x_values, y_values)
    plt.title("Fitness Function")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    
    plt.tight_layout()
    plt.show()

genetic_algorithm(fitness_function, x_min, x_max, popsize, generations, lchrom, pcross, pmutation)
