import configparser
import pygame
import Calculations

config = configparser.ConfigParser()
config.read('config.ini')
config_creature = config['CREATURE']


class Stealth:

    def __init__(self, creature):

        self.world = creature.world
        self.creature = creature
        self.species = creature.species
        self.type = "Stealth"

        self.objects_in_range = []
        self.predator_list = []
        self.cover = None
        self.find_cover()

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
                    if each not in self.objects_in_range:
                        self.objects_in_range.append(each)

    def get_predators(self):

        for each in self.world.object_container:
            if each.type is "Predator":
                self.predator_list.append(each)

    def find_cover(self):
        if len(self.objects_in_range) > 0:
            for each in self.world.object_container:
                if each.type is "Obstacle":

                    if self.cover is None:
                        self.cover = each
                    elif Calculations.get_distance(self.creature, each) < Calculations.get_distance(self.creature, self.cover):
                        self.cover = each

    def cohesion(self):

        total_positions = [self.creature.position[0], self.creature.position[1]]
        number_of_boids = 1

        for each in self.objects_in_range:
            if each.type is "Boid":
                if each.species is self.species:
                    number_of_boids += 1
                    total_positions[0] += each.position[0]
                    total_positions[1] += each.position[1]

        average_position = total_positions[0] / number_of_boids, total_positions[1] / number_of_boids

        if self.creature.position[0] > average_position[0]:
            self.creature.position = self.creature.position[0] - self.creature.turn_speed * 5, self.creature.position[1]
        else:
            self.creature.position = self.creature.position[0] + self.creature.turn_speed * 5, self.creature.position[1]
        if self.creature.position[1] > average_position[1]:
            self.creature.position = self.creature.position[0], self.creature.position[1] - self.creature.turn_speed * 5
        else:
            self.creature.position = self.creature.position[0], self.creature.position[1] + self.creature.turn_speed * 5


    def update(self):
        self.cohesion()
        self.move()





