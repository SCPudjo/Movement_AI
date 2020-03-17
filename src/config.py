WORLD = {
    'width': 800,
    'height': 600,
    'FPS': 120,
    'boids_per_species': 25,
    'number_of_stealth_pillars': 5
}

CREATURE = {
    'radius': 5,
    'movement_speed': 25,
    'turn_speed': 8,
    'vision': 50,
    # amount of space creature will attempt to maintain from other objects
    'distance': 20
}

PREDATOR = {
    'radius': 7,
    'movement_speed': 35,
    'turn_speed': 8,
    'vision': 75,
    'reach': 10,
    # amount of space predator will attempt to maintain from other objects
    'distance': 20
}

WALL = {
    'radius': 5,
    'size': 25,
    'r': 100,
    'g': 100,
    'b': 100
}

PILLAR = {
    'radius': 20,
    'r': 100,
    'g': 100,
    'b': 100
}

TARGET = {
    'radius': 15,
    'r': 50,
    'g': 50,
    'b': 200
}