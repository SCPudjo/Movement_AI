import random


class Fleeing:

    def __init__(self, creature):

        self.world = creature.world
        self.creature = creature
        self.species = creature.species
        self.type = "Wandering"
        self.wandering_direction = random.uniform(-1, 1), random.uniform(-1, 1)

        self.fleeing = False

    def move(self):

        pass

    def wander(self):

        pass

    # change direction by turning_speed based on new target direction
    def change_direction(self, target_direction):

        pass

    def separation(self):

        pass

    def update(self):

        pass

    # --------------------------------------------------
    #   Display Functions

    def display_range(self):

        pass

