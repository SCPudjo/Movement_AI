import configparser
import pygame

config = configparser.ConfigParser()
config.read('config.ini')
config_target = config['TARGET']

class Target:

    def __init__(self, world, x, y):

        self.world = world
        self.type = "Target"

        self.position = x, y
        self.radius = int(config_target['radius'])

        r = int(config_target['r'])
        g = int(config_target['g'])
        b = int(config_target['b'])

        self.colour = (r, g, b)

    # --------------------------------------------------
    #   Update Functions

    def update_position(self):

        pygame.draw.circle(self.world.surface,
                           self.colour,
                           (int(self.position[0]), int(self.position[1])),
                           self.radius,
                           1)

    def update(self):

        self.update_position()
