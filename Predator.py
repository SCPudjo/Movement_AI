import configparser
import pygame
import random
import Calculations

config = configparser.ConfigParser()
config.read('config.ini')
config_creature = config['PREDATOR']


class Predator:

    def __init__(self, world):

        self.world = world
        self.type = "Predator"

        self.vision = int(config_creature['vision'])
        self.movement_speed = int(config_creature['movement_speed'])
        self.turn_speed = float(config_creature['turn_speed']) / 100
        self.distance = int(config_creature['distance'])

        self.position = random.uniform(0, self.world.width), random.uniform(0, self.world.height)
        self.direction = (random.uniform(-1, 1), random.uniform(-1, 1))  # initialize random direction
        self.direction = Calculations.get_vector(self.direction)

        self.target_object = None

    def move(self):

        new_position = [self.position[0] + self.movement_speed * self.direction[0],
                        self.position[1] + self.movement_speed * self.direction[1]]

        if new_position[0] > self.world.width:
            new_position[0] = 0
        elif new_position[0] < 0:
            new_position[0] = self.world.width

        if new_position[1] > self.world.height:
            new_position[1] = 0
        elif new_position[1] < 0:
            new_position[1] = self.world.height

        self.position = new_position

    def hunt_target(self):
        if self.target_object is not None:
            target_position = self.target_object.position

            if self.position != target_position:

                if self.position[0] > target_position[0]:
                    self.position = self.position[0] - self.movement_speed, self.position[1]
                else:
                    self.position = self.position[0] + self.movement_speed, self.position[1]

                if self.position[1] > target_position[1]:
                    self.position = self.position[0], self.position[1] - self.movement_speed
                else:
                    self.position = self.position[0], self.position[1] + self.movement_speed


    def update_target(self):

        for each in self.world.object_container:
            if each.type is "Boid":
                if self.target_object is not None:
                    if Calculations.get_distance(self, self.target_object) > Calculations.get_distance(self, each):
                        self.target_object = each
                else:
                    self.target_object = each

    def update_position(self):

        pygame.draw.circle(self.world.surface, (255, 0, 0), (int(self.position[0]), int(self.position[1])), 8, 0)

    def update(self):

        self.update_target()
        self.display_target()
        self.hunt_target()
        self.move()
        self.update_position()

    def display_target(self):

        if self.target_object is not None:
            pygame.draw.line(self.world.surface, (255, 0, 0), self.position, self.target_object.position, 1)
