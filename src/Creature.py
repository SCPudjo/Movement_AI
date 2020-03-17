import pygame
import random
from src import Calculations
from src.behaviours.Wandering import Wandering
from .config import CREATURE


class Creature:

    def __init__(self, world, species):

        self.world = world
        self.type = "Creature"

        self.species = species
        print(self.species)

        self.radius = CREATURE['radius']
        self.vision = CREATURE['vision']
        self.movement_speed = float(CREATURE['movement_speed']) / 10
        self.turn_speed = float(CREATURE['turn_speed']) / 100
        self.distance = CREATURE['distance']

        self.position = (random.uniform(0, self.world.width), random.uniform(0, self.world.height))
        self.direction = (random.uniform(-1, 1), random.uniform(-1, 1))  # initialize random direction
        self.direction = Calculations.get_vector(self.direction)

        self.behaviour = Wandering(self)

    # --------------------------------------------------
    #   Display Functions

    def display_direction(self):

        pygame.draw.line(self.world.surface, self.species, self.position,
                         (self.position[0] + self.direction[0] * 10, self.position[1] + self.direction[1] * 10), 2)

    def display_range(self):

        pygame.draw.circle(self.world.surface, self.species, (int(self.position[0]), int(self.position[1])), self.vision, 1)


    # --------------------------------------------------
    #   Display Functions

    # updates actual visual position in the world
    def update_position(self):

        pygame.draw.circle(self.world.surface, self.species, (int(self.position[0]), int(self.position[1])), self.radius, 0)


    # updates called every frame
    def update(self):

        self.update_position()
        self.display_direction()
        self.behaviour.update()
