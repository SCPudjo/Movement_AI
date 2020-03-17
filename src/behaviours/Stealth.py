# flocking behaviour based on Craig Reynold's Boids, an artificial life program
# https://en.wikipedia.org/wiki/Boids#cite_note-5

import pygame
from src import Calculations


class Stealth:

    def __init__(self, creature):

        self.world = creature.world
        self.creature = creature
        self.species = creature.species
        self.type = "Flocking"

        self.avoid_collision = False
        self.closest_pillar = None
        self.predator = None

    # change position based on vector and movement speed
    def move(self):
        print(Calculations.get_distance(self.creature, self.closest_pillar))
        if Calculations.get_distance(self.creature, self.closest_pillar) > self.creature.distance + 20:

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

    def get_closest_pillar(self):

        self.closest_pillar = None
        for each in self.world.object_container:
            if each.type is "Obstacle":
                if self.closest_pillar is None:
                    self.closest_pillar = each
                elif Calculations.get_distance(self.creature, self.closest_pillar) > Calculations.get_distance(self.creature, each):
                    self.closest_pillar = each

    def get_closest_predator(self):

        self.predator = None
        for each in self.world.object_container:
            if each.type is "Predator":
                if self.closest_pillar is None:
                    self.closest_pillar = each
                elif Calculations.get_distance(self.creature, self.closest_pillar) > Calculations.get_distance(
                        self.creature, each):
                    self.closest_pillar = each

    def boid_flocking(self):

        self.avoid_collision = False
        for each in self.objects_in_range:
            if each.type is "Obstacle":
                if Calculations.get_distance(self.creature, each) < self.creature.vision:
                    self.avoid_collision = True
            elif each.type is "Creature":
                if Calculations.get_distance(self.creature, each) < self.creature.distance:
                    self.avoid_collision = True

        if self.avoid_collision:
            self.separation()
        else:
            self.cohesion()

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

    # steer to move towards the average position (center of mass) of local flockmates
    def cohesion(self):

        if self.closest_pillar is not None:

            if self.creature.position[0] > self.closest_pillar.position[0] and self.creature.position[1] > self.closest_pillar.position[1]:
                self.creature.direction = Calculations.rotate_vector(self.creature.direction, -self.creature.turn_speed,
                                                                     -self.creature.turn_speed)

            elif self.creature.position[0] > self.closest_pillar.position[0] and self.creature.position[1] < self.closest_pillar.position[
                1]:
                self.creature.direction = Calculations.rotate_vector(self.creature.direction, -self.creature.turn_speed,
                                                                     self.creature.turn_speed)

            elif self.creature.position[0] < self.closest_pillar.position[0] and self.creature.position[1] > self.closest_pillar.position[
                1]:
                self.creature.direction = Calculations.rotate_vector(self.creature.direction, self.creature.turn_speed,
                                                                     -self.creature.turn_speed)

            elif self.creature.position[0] < self.closest_pillar.position[0] and self.creature.position[1] < self.closest_pillar.position[
                1]:
                self.creature.direction = Calculations.rotate_vector(self.creature.direction, -self.creature.turn_speed,
                                                                     -self.creature.turn_speed)

    # --------------------------------------------------
    #   Update Functions

    def update(self):

        self.get_closest_pillar()
        self.get_closest_predator()
        #self.display_connection()
        self.cohesion()
        self.move()

    # --------------------------------------------------
    #   Display Functions

    def display_connection(self):

        pygame.draw.line(self.world.surface,
                         self.creature.species.value,
                         self.creature.position,
                         self.closest_pillar.position,
                         1)
