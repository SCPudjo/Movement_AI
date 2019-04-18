import configparser
import pygame
import random
import Calculations
from behaviours.Wandering import Wandering
from behaviours.Boid_Flocking import Boid_Flocking
config = configparser.ConfigParser()
config.read('config.ini')
config_creature = config['CREATURE']


class Creature:

    def __init__(self, world, species):

        self.world = world
        self.type = "Boid"

        self.species = species

        self.radius = int(config_creature['radius'])
        self.vision = int(config_creature['vision'])
        self.movement_speed = float(config_creature['movement_speed']) / 10
        self.turn_speed = float(config_creature['turn_speed']) / 100
        self.distance = int(config_creature['distance'])

        self.position = (random.uniform(0, self.world.width), random.uniform(0, self.world.height))
        self.direction = (random.uniform(-1, 1), random.uniform(-1, 1))  # initialize random direction
        self.direction = Calculations.get_vector(self.direction)

        self.behaviour = Boid_Flocking(self)

    # --------------------------------------------------
    #   Display Functions

    def display_direction(self):

        pygame.draw.line(self.world.surface, self.species.value, self.position,
                         (self.position[0] + self.direction[0] * 10, self.position[1] + self.direction[1] * 10), 2)

    def display_range(self):

        pygame.draw.circle(self.world.surface, self.species.value, (int(self.position[0]), int(self.position[1])), self.vision, 1)



    # --------------------------------------------------
    #   Display Functions

    # updates actual visual position in the world
    def update_position(self):

        pygame.draw.circle(self.world.surface, self.species.value, (int(self.position[0]), int(self.position[1])), self.radius, 0)


    # updates called every frame
    def update(self):

        self.update_position()
        self.display_direction()
        self.behaviour.update()
