import pygame
from .config import TARGET


class Target:

    def __init__(self, world, x, y):

        self.world = world
        self.type = "Target"

        self.position = x, y
        self.radius = TARGET['radius']

        r = TARGET['r']
        g = TARGET['g']
        b = TARGET['b']

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
