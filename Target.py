import pygame


class Target:

    def __init__(self, world, x, y):

        self.world = world
        self.type = "Target"

        self.position = x, y

    # --------------------------------------------------
    #   Update Functions

    def update_position(self):

        pygame.draw.circle(self.world.surface, (0, 0, 200), (int(self.position[0]), int(self.position[1])), 15, 1)

    def update(self):

        self.update_position()
