import matplotlib.pyplot as plt
import numpy as np


def plot_route(route, title, subplot_pos):
    plt.subplot(1, 2, subplot_pos)
    
    x_coords = [city.x for city in route.cities]
    y_coords = [city.y for city in route.cities]
    
    x_coords.append(x_coords[0])
    y_coords.append(y_coords[0])
    
    plt.plot(x_coords, y_coords, 'b-', zorder=1)
    plt.scatter(x_coords[:-1], y_coords[:-1], c='red', zorder=2)
    
    # Add city labels
    for city in route.cities:
        plt.annotate(city.name, (city.x, city.y), xytext=(5, 5), 
                    textcoords='offset points')
    
    plt.title(f"{title}\nCost: {route.travel_cost:.2f}")
    plt.grid(True)

def plot_final_routes(population):
    plt.figure(figsize=(12, 6))
    
    # Sort routes by fitness
    sorted_routes = sorted(population.routes, key=lambda x: x.fitness, reverse=True)
    
    # Plot best route
    plot_route(sorted_routes[0], "Best Route", 1)
    
    # Plot worst route
    plot_route(sorted_routes[-1], "Worst Route", 2)
    
    plt.tight_layout()
    plt.show()    

def plot_results(history): 
    plt.figure(figsize=(8, 6))
    gen_range = range(len(history["max_cost"]))
    
    plt.plot(gen_range, history["max_cost"], label="Max Cost")
    plt.plot(gen_range, history["min_cost"], label="Min Cost")
    plt.plot(gen_range, history["avg_cost"], label="Avg Cost")
    plt.title("Costs Across the Generations")
    plt.xlabel("Generation")
    plt.ylabel("Cost")
    plt.legend()
    plt.show()