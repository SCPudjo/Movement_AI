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

    def get_close_objects(self):

        self.objects_in_range = []
        for each in self.world.object_container:
            if each is not self:
                if Calculations.get_distance(self.creature, each) <= self.creature.vision:
                    if each not in self.objects_in_range:
                        self.objects_in_range.append(each)
                else:
                    if each in self.objects_in_range:
                        self.objects_in_range.remove(each)

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

    def alignment(self):

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

    def cohesion(self):

        for each in self.objects_in_range:
            if each.type is "Boid":
                if each.species is self.species:
                    mid_point = Calculations.get_midpoint(self.creature, each)
                    if self.creature.position != mid_point:
                        if self.creature.position[0] > mid_point[0]:
                            self.creature.position = self.creature.position[0] - self.creature.turn_speed * 2, self.creature.position[1]
                        else:
                            self.creature.position = self.creature.position[0] + self.creature.turn_speed * 2, self.creature.position[1]
                        if self.creature.position[1] > mid_point[1]:
                            self.creature.position = self.creature.position[0], self.creature.position[1] - self.creature.turn_speed * 2
                        else:
                            self.creature.position = self.creature.position[0], self.creature.position[1] + self.creature.turn_speed * 2

    def separation(self):

        for each in self.objects_in_range:
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

    # --------------------------------------------------
    #   Update Functions

    def update(self):

        self.get_close_objects()
        self.alignment()
        self.cohesion()
        self.separation()
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
