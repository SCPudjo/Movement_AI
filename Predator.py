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
        self.movement_speed = int(config_creature['movement_speed']) / 10
        self.turn_speed = float(config_creature['turn_speed']) / 100
        self.distance = int(config_creature['distance'])
        self.reach = int(config_creature['reach'])
        self.digestion_time = int(config_creature['digestion_time'])
        self.counter = 0

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

    def separation(self):

        for each in self.world.object_container:
            if each.type is "Obstacle":
                if Calculations.get_distance(self, each) < self.distance:

                    if self.position[0] > each.position[0] and self.position[0] - each.position[0] < self.distance:
                        self.position = self.position[0] + self.turn_speed * 10, self.position[1]
                    elif self.position[0] < each.position[0] and each.position[0] - self.position[0] < self.distance:
                        self.position = self.position[0] - self.turn_speed * 10, self.position[1]

                    if self.position[1] > each.position[1] and self.position[1] - each.position[1] < self.distance:
                        self.position = self.position[0], self.position[1] + self.turn_speed * 10
                    elif self.position[1] < each.position[1] and each.position[1] - self.position[1] < self.distance:
                        self.position = self.position[0], self.position[1] - self.turn_speed * 10

    def eat_target(self):

        if self.target_object is not None:

            if self.target_object in self.world.object_container:

                if Calculations.get_distance(self, self.target_object) < self.reach:
                    self.world.object_container.remove(self.target_object)
                    self.target_object = None
                    self.movement_speed /= 2

    def hunt_target(self):

        if self.target_object is not None:

            if self.target_object in self.world.object_container:

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
            else:
                self.target_object = None
        else:
            self.move()

    def update_target(self):
        self.target_object = None
        for each in self.world.object_container:
            if each.type is "Boid":
                if self.target_object is not None:
                    if Calculations.get_distance(self, self.target_object) > Calculations.get_distance(self, each):
                        self.target_object = each
                elif Calculations.get_distance(self, each) < self.vision:
                    self.target_object = each

    def update_position(self):

        pygame.draw.circle(self.world.surface, (255, 0, 0), (int(self.position[0]), int(self.position[1])), 8, 0)

    def restore_speed(self):
        if self.counter >= self.digestion_time:
            if self.movement_speed < int(config_creature['movement_speed']) / 10:
                self.movement_speed *= 2
                self.counter = 0

    def update(self):
        self.counter += 1
        self.update_target()
        self.display_target()
        self.separation()
        self.hunt_target()
        self.eat_target()
        self.restore_speed()
        self.update_position()

    def display_target(self):

        if self.target_object is not None:
            pygame.draw.line(self.world.surface, (255, 0, 0), self.position, self.target_object.position, 1)
