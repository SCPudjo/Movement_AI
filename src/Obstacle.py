import pygame
from .config import WALL, PILLAR


class Wall:

    def __init__(self, world, x, y):

        self.world = world
        self.type = "Obstacle"

        self.position = x, y
        self.radius = WALL['radius']

        r = WALL['r']
        g = WALL['g']
        b = WALL['b']

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
        self.radius = PILLAR['radius']

        r = PILLAR['r']
        g = PILLAR['g']
        b = PILLAR['b']

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
