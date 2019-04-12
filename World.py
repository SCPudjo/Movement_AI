import pygame, sys
import time
import configparser
from Creature import Creature

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

        self.update_counter = 0
        self.display_counter = 0

        #self.update_increment = 1
        #self.display_increment = 1
        self.time_start = time.time()

        for each in range(0, 25):
            self.object_container.append(Creature(self))

    def spawn_creature(self):

        self.object_container.append(Creature(self))


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

    if not paused:

        World.surface.fill(World.surface_color)

        for each in World.object_container:
            each.update()

        '''

        if World.update_counter >= World.FPS:

            World.surface.fill(World.surface_color)
            World.surface.blit(World.background, (0,0))

            for each in World.obstacle_container:
                each.update()

            for each in World.creature_container:
                each.update()

            
            if config_world['display_names'] == 'True':
                for each in World.creature_container:
                    font = pygame.font.Font('freesansbold.ttf', 20)
                    text = font.render(each.name, True, (100, 100, 100))
                    textRect = text.get_rect()
                    textRect.center = (each.body.world_movement.x_center, each.body.world_movement.y_center - 40)
                    World.surface.blit(text, textRect)
        
            World.update_counter = 0

        if World.display_counter >= World.FPS:
            if config_world['display_data'] == 'True':
                print("----------------------------------------")
                print("          W O R L D - S T A T S         ")
                print("----------------------------------------")
                print("Time Elapsed: " + str(round(time.time() - World.time_start, 0)) + " seconds")
                print("Creatures: " + str(World.creature_container))
                print("Obstacle: " + str(World.item_container))
                print("")
                
                for each in World.obstacle_container:
                    each.display_values()

                for each in World.creature_container:
                    pass

                for each in World.creature_container:
                    pass
                
                print("World Actions:")

            World.display_counter = 0
            
        '''

        pygame.display.update()
        pygame.time.Clock().tick(World.FPS)
        #World.update_counter += World.update_increment
        #World.display_counter += World.display_increment