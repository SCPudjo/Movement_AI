import configparser
import pygame

config = configparser.ConfigParser()
config.read('config.ini')
config_creature = config['CREATURE']


class Wall:

    def __init__(self, world, x, y):

        self.world = world
        self.type = "Obstacle"

        self.position = x, y

    # --------------------------------------------------
    #   Update Functions

    def update_position(self):

        pygame.draw.circle(self.world.surface, (160, 82, 45), (int(self.position[0]), int(self.position[1])), 5, 0)

    def update(self):

        self.update_position()

class Pillar:

    def __init__(self, world, x, y):

        self.world = world
        self.type = "Obstacle"

        self.position = x, y

    # --------------------------------------------------
    #   Update Functions

    def update_position(self):

        pygame.draw.circle(self.world.surface, (160, 82, 45), (int(self.position[0]), int(self.position[1])), 25, 0)

    def update(self):
        self.update_position()
