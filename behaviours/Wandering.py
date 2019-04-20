import configparser
import pygame
import random
import Calculations

config = configparser.ConfigParser()
config.read('config.ini')
config_creature = config['CREATURE']


class Wandering:

    def __init__(self, creature):

        self.world = creature.world
        self.creature = creature
        self.species = creature.species
        self.type = "Wandering"
        self.wandering_direction = random.uniform(-1, 1), random.uniform(-1, 1)

    def move(self):

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

    def wander(self):

        if random.uniform(0, 1) > 0.5:
            self.change_direction(self.wandering_direction)
            if random.uniform(0, 1) > 0.95:
                self.wandering_direction = random.uniform(-1, 1), random.uniform(-1, 1)


    # change direction by turning_speed based on new target direction
    def change_direction(self, target_direction):

        if self.creature.direction[0] > target_direction[0]:
            self.creature.direction = self.creature.direction[0] - self.creature.turn_speed, self.creature.direction[1]
        elif self.creature.direction[0] < target_direction[0]:
            self.creature.direction = self.creature.direction[0] + self.creature.turn_speed, self.creature.direction[1]
        if self.creature.direction[1] > target_direction[1]:
            self.creature.direction = self.creature.direction[0], self.creature.direction[1] - self.creature.turn_speed
        elif self.creature.direction[1] < target_direction[1]:
            self.creature.direction = self.creature.direction[0], self.creature.direction[1] + self.creature.turn_speed

    def separation(self):

        distance = 0

        for each in self.world.object_container:

            if each.type is "Obstacle":
                distance = self.creature.vision
            elif each.type is "Creature":
                distance = self.creature.distance

            if Calculations.get_distance(self.creature, each) <= 10:
                self.avoid_object(each, 1)
            elif Calculations.get_distance(self.creature, each) < distance / 5:
                self.avoid_object(each, self.creature.turn_speed)
            elif Calculations.get_distance(self.creature, each) < distance / 4:
                self.avoid_object(each, self.creature.turn_speed / 2)
            elif Calculations.get_distance(self.creature, each) < distance / 3:
                self.avoid_object(each, self.creature.turn_speed / 3)
            elif Calculations.get_distance(self.creature, each) < distance / 2:
                self.avoid_object(each, self.creature.turn_speed / 4)
            elif Calculations.get_distance(self.creature, each) < self.creature.vision:
                self.avoid_object(each, self.creature.turn_speed / 5)

    def avoid_object(self, object, turning_speed):

        if self.creature.position[0] > object.position[0] and self.creature.position[1] > object.position[1]:
            self.creature.direction = Calculations.rotate_vector(self.creature.direction, turning_speed, turning_speed)

        elif self.creature.position[0] > object.position[0] and self.creature.position[1] < object.position[1]:
            self.creature.direction = Calculations.rotate_vector(self.creature.direction, turning_speed, -turning_speed)

        elif self.creature.position[0] < object.position[0] and self.creature.position[1] > object.position[1]:
            self.creature.direction = Calculations.rotate_vector(self.creature.direction, -turning_speed, turning_speed)

        elif self.creature.position[0] < object.position[0] and self.creature.position[1] < object.position[1]:
            self.creature.direction = Calculations.rotate_vector(self.creature.direction, -turning_speed, -turning_speed)

    def update(self):

        #self.separation()
        self.wander()
        self.move()

    # --------------------------------------------------
    #   Display Functions

    def display_range(self):

        pygame.draw.circle(self.world.surface,
                           self.creature.species.value,
                           (int(self.creature.position[0]), int(self.creature.position[1])),
                           self.creature.vision,
                           1)
