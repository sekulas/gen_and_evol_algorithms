from gen_model import Population, City
from drawer import plot_final_routes, plot_results

cities = [
    City("A", 3, 3),
    City("B", 10, 9),
    City("C", 7, 7),
    City("D", 2, 9),
    City("E", 4, 8),
    City("F", 6, 8),
    City("G", 5, 4),
    City("H", 1, 6),
    City("I", 8, 5),
    City("J", 9, 2)
]
popsize = 20
generations = 200
pmutation = 0.01
pcross = 0.7

def update_history(history, population):
    max_cost, min_cost, avg_cost = population.get_travel_costs()
    history["max_cost"].append(max_cost)
    history["min_cost"].append(min_cost)
    history["avg_cost"].append(avg_cost)

if __name__ == "__main__":
    history = {
        "max_cost": [],
        "min_cost": [],
        "avg_cost": []
    }
    
    population = Population(Population.initialize_population(cities, popsize))
    
    update_history(history, population)

    for i in range(generations):
        population.reproduce(pmutation, pcross)
        update_history(history, population)
    
    plot_results(history)
    
    plot_final_routes(population)