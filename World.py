import pygame, sys
import time
import configparser
from Species import Species
from Creature import Creature
from Obstacle import Wall
from Obstacle import Pillar
from Target import Target
from behaviours.Idle import Idle
from behaviours.Wandering import Wandering
from behaviours.Boid_Flocking import Boid_Flocking
from behaviours.Targeted_Movement import Targeted_Movement
from behaviours.Stealth import Stealth
from behaviours.Predator import Predator

config = configparser.ConfigParser()
config.read('config.ini')
config_world = config['WORLD']

class World:

    def __init__(self):

        pygame.init()  # initiate pygame
        pygame.display.set_caption('Movement AI')

        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)

        pygame.key.set_repeat(500, 100)

        self.FPS = int(config_world['FPS'])

        self.object_container = []

        self.width = int(config_world['width'])
        self.height = int(config_world['height'])

        self.surface = pygame.display.set_mode((self.width, self.height))  # pygame.Surface object for the window
        self.surface_color = (150, 150, 150)
        self.surface.fill(self.surface_color)

        self.time_start = time.time()
        self.display_range = False

        self.boids_per_species = int(config_world['boids_per_species'])
        self.behaviour = "Wandering"

        self.spawn_objects_on_start()

    def spawn_objects_on_start(self):

        self.object_container = []

        for each in range(0, self.boids_per_species):
            self.object_container.append(Creature(self, Species.Cardinal))
            self.object_container.append(Creature(self, Species.Raven))

    def spawn_creature(self):

        cardinal = Creature(self, Species.Cardinal)
        self.object_container.append(cardinal)
        raven = Creature(self, Species.Raven)
        self.object_container.append(raven)

        if self.behaviour == "Idle":
            cardinal.behaviour = Idle(cardinal)
            raven.behaviour = Idle(raven)
        if self.behaviour == "Wandering":
            cardinal.behaviour = Wandering(cardinal)
            raven.behaviour = Wandering(raven)
        if self.behaviour == "Flocking":
            cardinal.behaviour = Boid_Flocking(cardinal)
            raven.behaviour = Boid_Flocking(raven)
        if self.behaviour == "Targeted Movement":
            cardinal.behaviour = Targeted_Movement(cardinal)
            raven.behaviour = Targeted_Movement(raven)

    def spawn_predator(self):

        self.despawn_predator()
        predator = Creature(self, Species.Eagle)
        predator.behaviour = Predator(predator)
        self.object_container.append(predator)

    def despawn_predator(self):

        for each in self.object_container:
            if each.behaviour.type is "Predator":
                self.object_container.remove(each)

    def spawn_target(self):

        self.despawn_target()
        x, y = pygame.mouse.get_pos()
        self.object_container.append(Target(self, x, y))

        for each in self.object_container:
            if each.type is "Creature":
                each.behaviour.target_reached = False

    def despawn_target(self):

        for each in self.object_container:
            if each.type is "Target":
                self.object_container.remove(each)
                break

World = World()
paused = False
counter = 0
display_counter = 0
fps = None

display_text = None

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

            # spawn a predator
            if event.key == pygame.K_p:
                World.spawn_predator()

            # spawn target
            if event.key == pygame.K_t and World.behaviour is "Targeted Movement":
                World.spawn_target()

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

            # set behaviour to Idle
            if event.key == pygame.K_1:
                World.behaviour = "Idle"
                World.despawn_target()
                for each in World.object_container:
                    if each.type is "Creature" and each.behaviour.type is not "Predator":
                        each.behaviour = Idle(each)

            # set behaviour to Wandering
            if event.key == pygame.K_2:
                World.behaviour = "Wandering"
                World.despawn_target()
                for each in World.object_container:
                    if each.type is "Creature" and each.behaviour.type is not "Predator":
                        each.behaviour = Wandering(each)

            # set behaviour to Boid Flocking
            if event.key == pygame.K_3:
                World.behaviour = "Flocking"
                World.despawn_target()
                for each in World.object_container:
                    if each.type is "Creature" and each.behaviour.type is not "Predator":
                        each.behaviour = Boid_Flocking(each)

            # set behaviour to Targeted_Movement
            if event.key == pygame.K_4:
                World.behaviour = "Targeted Movement"
                for each in World.object_container:
                    if each.type is "Creature" and each.behaviour.type is not "Predator":
                        each.behaviour = Targeted_Movement(each)

            # set behaviour to Stealth
            if event.key == pygame.K_5:
                World.behaviour = "Stealth"
                for each in World.object_container:
                    if each.type is "Creature" and each.behaviour.type is not "Predator":
                        each.behaviour = Stealth(each)

            # Reset
            if event.key == pygame.K_z:
                World.spawn_objects_on_start()
                World.behaviour = "Wandering"

            # ------------------------------
            #   Wall Generation Keys Start

            if event.key == pygame.K_KP1:
                x, y = pygame.mouse.get_pos()
                for each in range(0, 10):
                    World.object_container.append(Wall(World, x, y))
                    x -= 7
                    y += 7

            if event.key == pygame.K_KP2:
                x, y = pygame.mouse.get_pos()
                for each in range(0, 10):
                    World.object_container.append(Wall(World, x, y))
                    y += 10

            if event.key == pygame.K_KP3:
                x, y = pygame.mouse.get_pos()
                for each in range(0, 10):
                    World.object_container.append(Wall(World, x, y))
                    x += 7
                    y += 7

            if event.key == pygame.K_KP4:
                x, y = pygame.mouse.get_pos()
                for each in range(0, 10):
                    World.object_container.append(Wall(World, x, y))
                    x -= 10

            if event.key == pygame.K_KP5:
                x, y = pygame.mouse.get_pos()
                World.object_container.append(Pillar(World, x, y))

            if event.key == pygame.K_KP6:
                x, y = pygame.mouse.get_pos()
                for each in range(0, 10):
                    World.object_container.append(Wall(World, x, y))
                    x += 10

            if event.key == pygame.K_KP7:
                x, y = pygame.mouse.get_pos()
                for each in range(0, 10):
                    World.object_container.append(Wall(World, x, y))
                    x -= 7
                    y -= 7

            if event.key == pygame.K_KP8:
                x, y = pygame.mouse.get_pos()
                for each in range(0, 10):
                    World.object_container.append(Wall(World, x, y))
                    y -= 10

            if event.key == pygame.K_KP9:
                x, y = pygame.mouse.get_pos()
                for each in range(0, 10):
                    World.object_container.append(Wall(World, x, y))
                    x += 7
                    y -= 7

            # ------------------------------
            #   Wall Generation Keys End

    if not paused:

        while len(World.object_container) < World.boids_per_species * 2:
            World.spawn_creature()

        display_counter += 1

        frame_times = []
        start_t = time.time()

        World.surface.fill(World.surface_color)

        if World.display_range:
            for each in World.object_container:
                if each.type is "Creature" and each.behaviour.type == "Flocking":
                    pass #each.behaviour.display_range()

        for each in World.object_container:
            each.update()
            #print(each.behaviour)

        if display_counter == 10:
            display_text = World.behaviour + " | " + str(round(fps, 2))
            display_counter = 0

        # display text in top left
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(display_text, True, (255,255,255))
        textRect = text.get_rect()
        textRect.midleft = (25, 25)
        World.surface.blit(text, textRect)

        pygame.display.update()
        pygame.time.Clock().tick(World.FPS)


        end_t = time.time()
        time_taken = end_t - start_t
        start_t = end_t
        frame_times.append(time_taken)
        frame_times = frame_times[-20:]
        fps = len(frame_times) / sum(frame_times)

