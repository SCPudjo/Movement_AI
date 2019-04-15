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

        self.predator_list = []

    def get_predators(self):

        for each in self.world.object_container:
            if each.type is "Predator":
                self.predator_list.append(each)

    def find_cover(self):

        for each in self.world.object_container:
            if each.type is "Obstacle":
                pass



