import configparser
import pygame

config = configparser.ConfigParser()
config.read('config.ini')
config_wall = config['WALL']
config_pillar = config['PILLAR']


class Wall:

    def __init__(self, world, x, y):

        self.world = world
        self.type = "Obstacle"

        self.position = x, y
        self.radius = int(config_wall['radius'])

        r = int(config_wall['r'])
        g = int(config_wall['g'])
        b = int(config_wall['b'])

        self.colour = (r, g, b)

    # --------------------------------------------------
    #   Update Functions

    def update_position(self):

        pygame.draw.circle(self.world.surface,
                           self.colour,
                           (int(self.position[0]), int(self.position[1])),
                           self.radius,
                           0)

    def update(self):

        self.update_position()

class Pillar:

    def __init__(self, world, x, y):

        self.world = world
        self.type = "Obstacle"

        self.position = x, y
        self.radius = int(config_pillar['radius'])

        r = int(config_pillar['r'])
        g = int(config_pillar['g'])
        b = int(config_pillar['b'])

        self.colour = (r, g, b)

    # --------------------------------------------------
    #   Update Functions

    def update_position(self):

        pygame.draw.circle(self.world.surface,
                           self.colour,
                           (int(self.position[0]), int(self.position[1])),
                           self.radius,
                           0)

    def update(self):
        self.update_position()
