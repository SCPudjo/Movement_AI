# flocking behaviour based on Craig Reynold's Boids, an artificial life program
# https://en.wikipedia.org/wiki/Boids#cite_note-5

import configparser
import pygame
import Calculations

config = configparser.ConfigParser()
config.read('config.ini')
config_creature = config['PREDATOR']


class Predator:

    def __init__(self, creature):

        self.world = creature.world
        self.creature = creature
        self.species = creature.species
        self.type = "Predator"
        self.objects_in_range = []
        self.prey = None
        self.reach = int(config_creature['reach'])

        self.creature.radius = int(config_creature['radius'])
        self.creature.vision = int(config_creature['vision'])
        self.creature.movement_speed = float(config_creature['movement_speed']) / 10
        self.creature.turn_speed = float(config_creature['turn_speed']) / 100
        self.creature.distance = int(config_creature['distance'])

        self.avoid_collision = False

    # change position based on vector and movement speed
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

    # add all objects within creature's vision to objects_in_range array
    def get_close_objects(self):

        self.objects_in_range = []
        for each in self.world.object_container:
            if each is not self.creature:
                if Calculations.get_distance(self.creature, each) <= self.creature.vision:
                    self.objects_in_range.append(each)

    def get_prey(self):

        self.prey = None
        for each in self.objects_in_range:
            if each.type is "Creature":
                if each.species is not self.species:
                    if self.prey is None:
                        self.prey = each
                    elif Calculations.get_distance(self.creature, each) < Calculations.get_distance(self.creature,self.prey):
                        self.prey = each

    def eat_prey(self):
        if self.prey is not None:
            if Calculations.get_distance(self.creature, self.prey) <= self.reach:
                self.world.object_container.remove(self.prey)
                self.prey = None

    def boid_flocking(self):

        self.avoid_collision = False
        for each in self.objects_in_range:
            if each.type is "Obstacle":
                if Calculations.get_distance(self.creature, each) < self.creature.vision:
                    self.avoid_collision = True

        if self.avoid_collision:
            self.separation()
        else:
            self.cohesion()

    # steer towards closest non-predator creature, similar to boid flocking cohesion behaviour
    def cohesion(self):

        if self.prey is not None:

            if self.creature.position[0] > self.prey.position[0] and self.creature.position[1] > self.prey.position[1]:
                self.creature.direction = Calculations.rotate_vector(self.creature.direction, -self.creature.turn_speed, -self.creature.turn_speed)

            elif self.creature.position[0] > self.prey.position[0] and self.creature.position[1] < self.prey.position[1]:
                self.creature.direction = Calculations.rotate_vector(self.creature.direction, -self.creature.turn_speed, self.creature.turn_speed)

            elif self.creature.position[0] < self.prey.position[0] and self.creature.position[1] > self.prey.position[1]:
                self.creature.direction = Calculations.rotate_vector(self.creature.direction, self.creature.turn_speed, -self.creature.turn_speed)

            elif self.creature.position[0] < self.prey.position[0] and self.creature.position[1] < self.prey.position[1]:
                self.creature.direction = Calculations.rotate_vector(self.creature.direction, -self.creature.turn_speed, -self.creature.turn_speed)

    # steer to avoid obstacles and other predators
    def separation(self):

        for each in self.world.object_container:

            if each.type is "Obstacle":
                distance = each.radius
            elif each.type is "Creature":
                if each.species is self.species:
                    distance = self.creature.distance

            if Calculations.get_distance(self.creature, each) <= distance * 2:
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

    # --------------------------------------------------
    #   Update Functions

    def update(self):


        self.get_close_objects()
        self.get_prey()
        self.display_connection()
        self.boid_flocking()
        self.eat_prey()
        self.move()
        #print(self.creature.radius)

    # --------------------------------------------------
    #   Display Functions

    def display_connection(self):
        if self.prey is not None:
            pygame.draw.line(self.world.surface,
                             self.creature.species.value,
                             self.creature.position,
                             self.prey.position,
                             1)
