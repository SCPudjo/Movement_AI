# flocking behaviour based on Craig Reynold's Boids, an artificial life program
# https://en.wikipedia.org/wiki/Boids#cite_note-5

import configparser
import pygame
import Calculations

config = configparser.ConfigParser()
config.read('config.ini')
config_creature = config['CREATURE']


class Boid_Flocking:

    def __init__(self, creature):

        self.world = creature.world
        self.creature = creature
        self.species = creature.species
        self.type = "Flocking"
        self.objects_in_range = []

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
                    if each not in self.objects_in_range:
                        self.objects_in_range.append(each)

    def boid_flocking(self):
        '''
        for each in self.objects_in_range:
            if Calculations.get_distance(self.creature, each) < self.creature.distance and each.species is not self.species:
                self.avoid_collision = True

        if self.avoid_collision:
            self.separation()
        else:
            self.avoid_collision = False
            self.cohesion()
            self.alignment()
        '''
        self.separation()
        self.cohesion()
        self.alignment()

    # change direction by turning_speed based on new target direction
    def change_direction(self, target_direction):
        '''
        target_direction = (0, 0)

        if alignment is None and cohesion is None:
            return

        if cohesion is not None:
            target_direction = target_direction[0] + cohesion[0], cohesion[1] + target_direction[1]
        elif alignment is not None:
            target_direction = target_direction[0] + alignment[0], alignment[1] + target_direction[1]
        '''

        if self.creature.direction[0] > target_direction[0]:
            self.creature.direction = self.creature.direction[0] - self.creature.turn_speed, self.creature.direction[1]
        elif self.creature.direction[0] < target_direction[0]:
            self.creature.direction = self.creature.direction[0] + self.creature.turn_speed, self.creature.direction[1]

        if self.creature.direction[1] > target_direction[1]:
            self.creature.direction = self.creature.direction[0], self.creature.direction[1] - self.creature.turn_speed
        elif self.creature.direction[1] < target_direction[1]:
            self.creature.direction = self.creature.direction[0], self.creature.direction[1] + self.creature.turn_speed

    # steer towards the average heading of local flockmates
    def alignment(self):
        '''
        total_direction = [self.creature.direction[0], self.creature.direction[1]]
        number_of_boids = 1

        for each in self.objects_in_range:
            if each.type is "Boid":
                if each.species is self.species:
                    total_direction[0] += each.direction[0]
                    total_direction[1] += each.direction[1]
                    number_of_boids += 1

        if number_of_boids == 1:
            return None

        average_direction = total_direction[0] / number_of_boids, total_direction[1] / number_of_boids
        average_direction = Calculations.get_vector(average_direction)
        return average_direction
        '''

        total_direction = [self.creature.direction[0], self.creature.direction[1]]
        number_of_boids = 1

        for each in self.objects_in_range:
            if each.type is "Boid":
                if each.species is self.species:
                    total_direction[0] += each.direction[0]
                    total_direction[1] += each.direction[1]
                    number_of_boids += 1

        average_direction = total_direction[0] / number_of_boids, total_direction[1] / number_of_boids
        average_direction = Calculations.get_vector(average_direction)
        if self.creature.direction != average_direction:
            self.change_direction(average_direction)

    # steer to move towards the average position (center of mass) of local flockmates
    def cohesion(self):
        '''
        total_positions = [self.creature.position[0], self.creature.position[1]]
        number_of_boids = 1
        print(number_of_boids)

        for each in self.objects_in_range:
            if each.type is "Boid":
                if each.species is self.species:
                    number_of_boids += 1
                    print(number_of_boids)
                    total_positions[0] += each.position[0]
                    total_positions[1] += each.position[1]

        if number_of_boids == 1:
            print("returned")
            return None

        average_position = total_positions[0] / number_of_boids, total_positions[1] / number_of_boids
        target_direction = average_position[0] - self.creature.position[0], average_position[1] - self.creature.position[1]
        target_direction = Calculations.get_vector(target_direction)
        return target_direction
        '''

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

    # steer to avoid crowding local flockmates
    def separation(self):

        for each in self.objects_in_range:
            if Calculations.get_distance(self.creature, each) < self.creature.distance:

                if self.creature.position[0] > each.position[0] and self.creature.position[0] - each.position[0] < self.creature.distance:
                    self.creature.position = self.creature.position[0] + self.creature.turn_speed * 10, self.creature.position[1]
                elif self.creature.position[0] < each.position[0] and each.position[0] - self.creature.position[0] < self.creature.distance:
                    self.creature.position = self.creature.position[0] - self.creature.turn_speed * 10, self.creature.position[1]

                if self.creature.position[1] > each.position[1] and self.creature.position[1] - each.position[1] < self.creature.distance:
                    self.creature.position = self.creature.position[0], self.creature.position[1] + self.creature.turn_speed * 10
                elif self.creature.position[1] < each.position[1] and each.position[1] - self.creature.position[1] < self.creature.distance:
                    self.creature.position = self.creature.position[0], self.creature.position[1] - self.creature.turn_speed * 10

    # --------------------------------------------------
    #   Update Functions

    def update(self):

        self.get_close_objects()
        self.boid_flocking()
        self.display_connection()
        self.move()

    # --------------------------------------------------
    #   Display Functions

    def display_range(self):

        pygame.draw.circle(self.world.surface, self.creature.species.value, (int(self.creature.position[0]), int(self.creature.position[1])), self.creature.vision, 1)

    def display_connection(self):

        for each in self.objects_in_range:
            if each.type is "Boid" and each.species is self.species:
                pygame.draw.line(self.world.surface, self.creature.species.value, self.creature.position, each.position, 1)
