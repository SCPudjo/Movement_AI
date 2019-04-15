import configparser
import pygame
import random
import Calculations
from behaviours.Wandering import Wandering
from behaviours.Idle import Idle

config = configparser.ConfigParser()
config.read('config.ini')
config_creature = config['CREATURE']

class Creature:

    def __init__(self, world, species):

        self.world = world
        self.type = "Boid"

        self.species = species

        self.vision = int(config_creature['vision'])
        self.movement_speed = float(config_creature['movement_speed']) / 10
        self.turn_speed = float(config_creature['turn_speed']) / 100
        self.distance = int(config_creature['distance'])

        self.position = random.uniform(0, self.world.width), random.uniform(0, self.world.height)
        self.direction = (random.uniform(-1, 1), random.uniform(-1, 1))  # initialize random direction
        self.direction = Calculations.get_vector(self.direction)

        self.behaviour = Idle(self)

    def update_position(self):

        pygame.draw.circle(self.world.surface, self.species.value, (int(self.position[0]), int(self.position[1])), 5, 0)

    def update(self):

        self.update_position()
        self.behaviour.update()
