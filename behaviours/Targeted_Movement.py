import configparser
import pygame
import random
import Calculations

config = configparser.ConfigParser()
config.read('config.ini')
config_creature = config['CREATURE']


class Targeted_Movement:

    def __init__(self, creature):

        self.world = creature.world
        self.creature = creature
        self.species = creature.species
        self.type = "Wandering"
        self.target = None
        self.target_reached = False

    def get_target(self):

        for each in self.world.object_container:
            if each.type is "Target":
                self.target = each
                break
            else:
                self.target = None

    def move_to_target(self):

        if self.target is not None:

            self.target_reached = False

            if self.creature.position != self.target.position:

                if self.creature.position[0] > self.target.position[0]:
                    self.creature.position = self.creature.position[0] - self.creature.movement_speed, self.creature.position[1]
                elif self.creature.position[0] < self.target.position[0]:
                    self.creature.position = self.creature.position[0] + self.creature.movement_speed, self.creature.position[1]

                if self.creature.position[1] > self.target.position[1]:
                    self.creature.position = self.creature.position[0], self.creature.position[1] - self.creature.movement_speed
                elif self.creature.position[1] < self.target.position[1]:
                    self.creature.position = self.creature.position[0], self.creature.position[1] + self.creature.movement_speed

    def reach_target(self):

        if self.target is not None and not self.target_reached:

            if Calculations.get_distance(self.creature, self.target) < 10:
                self.target = None
                self.target_reached = True

            for each in self.world.object_container:

                if each.type is "Boid":
                    if Calculations.get_distance(self.creature, each) < 20 and each.behaviour.target_reached:
                        self.target = None
                        self.target_reached = True



    def separation(self):

        #if self.target is not None:
            for each in self.world.object_container:
                if each.type is "Boid" or each.type is "Obstacle":
                    if Calculations.get_distance(self.creature, each) < self.creature.distance:

                        if self.creature.position[0] > each.position[0] and self.creature.position[0] - each.position[0] < self.creature.distance:
                            self.creature.position = self.creature.position[0] + self.creature.turn_speed * 10, self.creature.position[1]
                        elif self.creature.position[0] < each.position[0] and each.position[0] - self.creature.position[0] < self.creature.distance:
                            self.creature.position = self.creature.position[0] - self.creature.turn_speed * 10, self.creature.position[1]

                        if self.creature.position[1] > each.position[1] and self.creature.position[1] - each.position[1] < self.creature.distance:
                            self.creature.position = self.creature.position[0], self.creature.position[1] + self.creature.turn_speed * 10
                        elif self.creature.position[1] < each.position[1] and each.position[1] - self.creature.position[1] < self.creature.distance:
                            self.creature.position = self.creature.position[0], self.creature.position[1] - self.creature.turn_speed * 10

    def update(self):

        self.get_target()
        self.move_to_target()
        self.reach_target()
        self.separation()

    # --------------------------------------------------
    #   Display Functions

    def display_range(self):

        pygame.draw.circle(self.world.surface, self.creature.species.value, (int(self.creature.position[0]), int(self.creature.position[1])), self.creature.vision, 1)
