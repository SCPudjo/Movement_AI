import pygame, sys
import time
import configparser
from Species import Species
from Creature import Creature
from Predator import Predator
from Obstacle import Wall
from Obstacle import Pillar
from behaviours.Idle import Idle
from behaviours.Wandering import Wandering
from behaviours.Boid_Flocking import Boid_Flocking

config = configparser.ConfigParser()
config.read('config.ini')
config_world = config['WORLD']

class World:

    def __init__(self):

        pygame.init()  # initiate pygame
        pygame.display.set_caption('Movement AI')
        pygame.key.set_repeat(500, 100)

        self.FPS = int(config_world['FPS'])

        self.object_container = []

        self.width = int(config_world['width'])
        self.height = int(config_world['height'])

        self.surface = pygame.display.set_mode((self.width, self.height))  # pygame.Surface object for the window
        self.surface_color = (245, 245, 220)
        self.surface.fill(self.surface_color)

        self.time_start = time.time()
        self.display_range = False

        self.spawn_objects_on_start()

    def spawn_objects_on_start(self):

        self.object_container = []

        for each in range(0, 20):
            self.object_container.append(Creature(self, Species.Cardinal))
            self.object_container.append(Creature(self, Species.Raven))

    def spawn_creature(self):

        self.object_container.append(Creature(self, Species.Cardinal))
        self.object_container.append(Creature(self, Species.Raven))

    def spawn_predator(self):

        self.object_container.append(Predator(self))


World = World()
paused = False

while True:  # main game loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # pause / unpause
            if event.key == pygame.K_SPACE:
                if paused is True:
                    paused = False
                    print("----------------------------------------")
                    print("   S I M U L A T I O N - R E S U M E D  ")
                    print("----------------------------------------")
                else:
                    paused = True
                    print("----------------------------------------")
                    print("   S I M U L A T I O N - P A U S E D    ")
                    print("----------------------------------------")

        if event.type == pygame.KEYDOWN and not paused:

            # spawn a creature
            if event.key == pygame.K_s:
                World.spawn_creature()

            # spawn a creature
            if event.key == pygame.K_p:
                World.spawn_predator()

            # remove all obstacles
            if event.key == pygame.K_o:

                num = len(World.object_container)
                counter = 0

                while counter < num:
                    if World.object_container[counter].type is "Obstacle":
                        World.object_container.pop(counter)
                        num = len(World.object_container)
                    else:
                        counter += 1

            if event.key == pygame.K_1:
                for each in World.object_container:
                    if each.type is "Boid":
                        each.behaviour = Idle(each)

            if event.key == pygame.K_2:
                for each in World.object_container:
                    if each.type is "Boid":
                        each.behaviour = Wandering(each)

            if event.key == pygame.K_3:
                for each in World.object_container:
                    if each.type is "Boid":
                        each.behaviour = Boid_Flocking(each)

            if event.key == pygame.K_z:
                World.spawn_objects_on_start()

            # ------------------------------
            #   Wall Generation Keys Start

            if event.key == pygame.K_KP1:
                x, y = pygame.mouse.get_pos()
                for each in range(0, 21):
                    World.object_container.append(Wall(World, x, y))
                    x -= 5
                    y += 5

            if event.key == pygame.K_KP2:
                x, y = pygame.mouse.get_pos()
                for each in range(0, 21):
                    World.object_container.append(Wall(World, x, y))
                    y += 5

            if event.key == pygame.K_KP3:
                x, y = pygame.mouse.get_pos()
                for each in range(0, 21):
                    World.object_container.append(Wall(World, x, y))
                    x += 5
                    y += 5

            if event.key == pygame.K_KP4:
                x, y = pygame.mouse.get_pos()
                for each in range(0, 21):
                    World.object_container.append(Wall(World, x, y))
                    x -= 5

            if event.key == pygame.K_KP5:
                x, y = pygame.mouse.get_pos()
                World.object_container.append(Pillar(World, x, y))

            if event.key == pygame.K_KP6:
                x, y = pygame.mouse.get_pos()
                for each in range(0, 21):
                    World.object_container.append(Wall(World, x, y))
                    x += 5

            if event.key == pygame.K_KP7:
                x, y = pygame.mouse.get_pos()
                for each in range(0, 21):
                    World.object_container.append(Wall(World, x, y))
                    x -= 5
                    y -= 5

            if event.key == pygame.K_KP8:
                x, y = pygame.mouse.get_pos()
                for each in range(0, 21):
                    World.object_container.append(Wall(World, x, y))
                    y += -5

            if event.key == pygame.K_KP9:
                x, y = pygame.mouse.get_pos()
                for each in range(0, 21):
                    World.object_container.append(Wall(World, x, y))
                    x += 5
                    y -= 5

            # ------------------------------
            #   Wall Generation Keys End

    if not paused:

        World.surface.fill(World.surface_color)

        if World.display_range:
            for each in World.object_container:
                if each.type is "Boid":
                    pass

        for each in World.object_container:
            each.update()
            #print(each.behaviour)

        pygame.display.update()
        pygame.time.Clock().tick(World.FPS)
