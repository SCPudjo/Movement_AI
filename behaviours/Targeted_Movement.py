import configparser
import pygame
import random
import Calculations
from Species import Species

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

        self.old_species = creature.species
        self.counter = 0

    # returns instance of targett
    def get_target(self):

        for each in self.world.object_container:
            if each.type is "Target":
                self.target = each
                break
            else:
                self.target = None

    # moves creature towards target if target is found
    def move(self):
        if not self.target_reached and self.target is not None:

            new_direction = (self.target.position[0] - self.creature.position[0],
                             self.target.position[1] - self.creature.position[1])

            self.creature.direction = Calculations.get_vector(new_direction)

            new_position = [self.creature.position[0] + self.creature.movement_speed * self.creature.direction[0],
                            self.creature.position[1] + self.creature.movement_speed * self.creature.direction[1]]

            if new_position[0] > self.world.width:
                new_position[0] = 0
            elif new_position[0] < 0:
                new_position[0] = self.world.width
            if new_position[1] > self.world.height:
                new_position[1] = 0
            elif new_position[1] < 0:
                new_position[1] = self.world.height
            self.creature.position = new_position

    def reach_target(self):

        if self.target is not None and not self.target_reached:
            if Calculations.get_distance(self.creature, self.target) < 5:
                self.target = None
                self.target_reached = True
                self.creature.species = Species.Goldfinch

            for each in self.world.object_container:

                if each.type is "Creature":
                    if Calculations.get_distance(self.creature, each) < 10 and each.behaviour.target_reached:
                        self.target = None
                        self.target_reached = True
                        self.creature.species = Species.Goldfinch


    def separation(self):

        #if self.target is not None:
            for each in self.world.object_container:
                if each.type is "Creature" or each.type is "Obstacle":
                    if Calculations.get_distance(self.creature, each) < self.creature.distance:

                        if self.creature.position[0] > each.position[0] and self.creature.position[0] - each.position[0] < self.creature.distance:
                            self.creature.position = self.creature.position[0] + self.creature.turn_speed * 10, self.creature.position[1]
                        elif self.creature.position[0] < each.position[0] and each.position[0] - self.creature.position[0] < self.creature.distance:
                            self.creature.position = self.creature.position[0] - self.creature.turn_speed * 10, self.creature.position[1]

                        if self.creature.position[1] > each.position[1] and self.creature.position[1] - each.position[1] < self.creature.distance:
                            self.creature.position = self.creature.position[0], self.creature.position[1] + self.creature.turn_speed * 10
                        elif self.creature.position[1] < each.position[1] and each.position[1] - self.creature.position[1] < self.creature.distance:
                            self.creature.position = self.creature.position[0], self.creature.position[1] - self.creature.turn_speed * 10

    def magic(self):
        if self.creature.species is not self.old_species:
            self.counter += 1
            pygame.draw.circle(self.world.surface,
                               (255, 223, 0),
                               (int(self.creature.position[0]), int(self.creature.position[1])),
                               self.counter,
                               1)
            if self.counter >= 50:
                self.creature.species = self.old_species
                self.counter = 0

    def update(self):

        self.get_target()
        self.move()
        self.reach_target()
        self.separation()
        self.magic()

    # --------------------------------------------------
    #   Display Functions

    def display_range(self):

        pygame.draw.circle(self.world.surface,
                           self.creature.species.value,
                           (int(self.creature.position[0]), int(self.creature.position[1])),
                           self.creature.vision,
                           1)
