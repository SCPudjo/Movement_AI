import configparser
import pygame
import math
import random
import Calculations

config = configparser.ConfigParser()
config.read('config.ini')
config_creature = config['CREATURE']


class Creature:

    def __init__(self, world):

        self.world = world
        self.type = "Boid"
        self.vision = int(config_creature['vision'])
        self.movement_speed = int(config_creature['movement_speed'])
        self.turn_speed = int(config_creature['turn_speed']) / 10
        self.distance = int(config_creature['distance'])

        self.position = random.uniform(0, self.world.width), random.uniform(0, self.world.height)
        self.direction = (random.uniform(-1, 1), random.uniform(-1, 1)) # initialize random direction
        self.direction = Calculations.get_vector(self.direction)

        self.objects_in_range = []

    def move(self):

        new_position = [self.position[0] + self.movement_speed * self.direction[0], self.position[1] + self.movement_speed * self.direction[1]]

        if new_position[0] > self.world.width:
            new_position[0] = 0
        elif new_position[0] < 0:
            new_position[0] = self.world.width

        if new_position[1] > self.world.height:
            new_position[1] = 0
        elif new_position[1] < 0:
            new_position[1] = self.world.height

        self.position = new_position

    def update_position(self):

        pygame.draw.circle(self.world.surface, (0, 0, 0), (int(self.position[0]), int(self.position[1])), 5, 0)

    def alignment(self):

        '''
        total_direction = []

        for each in self.objects_in_range:
            if each.type is "Boid":
                total_direction.append(each.direction)

        average_direction = [0,0]

        if len(total_direction) > 0:
            for each in total_direction:
                average_direction[0] += each[0]
                average_direction[1] += each[1]
            average_direction[0] /= len(total_direction)
            average_direction[1] /= len(total_direction)

            average_direction = Calculations.get_vector((average_direction[0], average_direction[1]))
            self.direction = average_direction

        '''

        #'''
        for each in self.objects_in_range:
            if each.type is "Boid":
                average_vector = Calculations.get_average_vector(self.direction, each.direction)
                if self.direction != average_vector:
                    self.direction = average_vector
                #pygame.draw.line(self.world.surface, (255, 0, 0), self.position, each.position, 1)
        #'''

    def cohesion(self):

        for each in self.objects_in_range:
            if each.type is "Boid":
                mid_point = Calculations.get_midpoint(self, each)
                if self.position != mid_point:

                    if self.position[0] > mid_point[0]:
                        self.position = self.position[0] - self.turn_speed, self.position[1]
                    else:
                        self.position = self.position[0] + self.turn_speed, self.position[1]

                    if self.position[1] > mid_point[1]:
                        self.position = self.position[0], self.position[1] - self.turn_speed
                    else:
                        self.position = self.position[0], self.position[1] + self.turn_speed

    def separation(self):

        for each in self.objects_in_range:
            if each.type is "Boid":

                if Calculations.get_distance(self, each) < self.distance:

                    if abs(self.position[0]) - abs(each.position[0]) < self.distance:
                        if self.position[0] > each.position[0]:
                            self.position = self.position[0] + 0.5, self.position[1]
                        else:
                            self.position = self.position[0] - 0.5, self.position[1]

                    if abs(self.position[1]) - abs(each.position[1]) < self.distance:
                        if self.position[1] > each.position[1]:
                            self.position = self.position[0], self.position[1] + 0.5
                        else:
                            self.position = self.position[0], self.position[1] - 0.5


    def get_close_objects(self):

        for each in self.world.object_container:
            if each is not self:
                if Calculations.get_distance(self, each) <= self.vision:
                    if each not in self.objects_in_range:
                        self.objects_in_range.append(each)
                else:
                    if each in self.objects_in_range:
                        self.objects_in_range.remove(each)

    def display_range(self):

        pygame.draw.circle(self.world.surface, (255, 0, 0), (int(self.position[0]), int(self.position[1])), self.vision, 1)

    def update(self):

        self.update_position()
        self.get_close_objects()
        self.alignment()
        self.cohesion()
        self.separation()
        self.move()
        #self.display_range()
        #print(self.direction)
        #print(self.objects_in_range)


