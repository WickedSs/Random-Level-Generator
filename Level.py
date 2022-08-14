from itertools import count
import queue
from tracemalloc import start
from typing import NewType
from pygame.math import Vector2
import sys, os, pygame, numpy, random, time, string
from Settings import *
import operator


alphabet = string.ascii_letters
ROOT = os.path.dirname(sys.modules['__main__'].__file__)
GRID = []
VISITED = []

class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, name, image, sprites):
        super().__init__()
        self.sprites = sprites
        self.x, self.y = x, y
        self.name = name
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.queued = False
        self.visited = False
        self.neighbours, self.next_sprites = {0 : [], 1 : [], 2 : [], 3 : []}
        self.sides = self.sprites[self.name]["Sides"]
        self.color_labels = {}

    def set_neighbours(self):
        x, y = int(self.x / TILE_SIZE), int(self.y / TILE_SIZE)
        if x > 0:
            self.neighbours.append(GRID[y][x - 1])
        
        if x < (SCREEN_WIDTH / TILE_SIZE) - 1:
            self.neighbours.append(GRID[y][x + 1])
        
        if y > 0:
            self.neighbours.append(GRID[y - 1][x])

        if y < (SCREEN_HEIGHT  / TILE_SIZE) - 1:
            self.neighbours.append(GRID[y + 1][x])

    def setPossibleNeighbours(self):
        for key in self.sprites.keys():
            sides = self.sprites[key]["Sides"]
            for i in range(len(sides)):
                if self.sides[i] == sides[i]:
                    self.next_sprites[i].append(key)
    
    def updateSprite(self, image, name):
        self.name = name
        self.image = image

    def getPosition(self):
        return (int(self.x/TILE_SIZE), int(self.y/TILE_SIZE))
    


class Level:
    spritesheet_filename = os.path.join(ROOT, "Assets/Spritesheet.png")
    def __init__(self):
        self.sprite_sheet = pygame.image.load(self.spritesheet_filename).convert_alpha()
        self.display_surface = pygame.display.get_surface()
        self.level_sprites = pygame.sprite.Group()
        self.queue, self.sprites = [], {}
        self.layout_in_use = "First_Layout"
        self.initialize_generation()
        

    def get_sprite(self, Position):
        sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet, (0, 0), (Position[0], Position[1], TILE_SIZE, TILE_SIZE))
        return sprite
    
    def process_sides(self, pxarray):
        self.sides[0].extend(pxarray[0])
        self.sides[2].extend(pxarray[31])
        self.sides[1].extend(array[0] for array in pxarray)
        self.sides[3].extend(array[31] for array in pxarray)
    
    def convert_pixelarray(self, pxarray):
        array = []
        for i in range(len(pxarray)):
            array.append([])
            for j in range(len(pxarray[i])):
                array[i].append(pxarray[i][j])
        
        return array
    
    def initialize_grid(self):
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            GRID.append([])
            for x in range(0, SCREEN_WIDTH, TILE_SIZE):
                sprite = Sprite(x, y)
                self.level_sprites.add(sprite)
                GRID[int(y/TILE_SIZE)].append(sprite)
        
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for x in range(0, SCREEN_WIDTH, TILE_SIZE):
                GRID[int(y/TILE_SIZE)][int(x/TILE_SIZE)].set_neighbours()
                GRID[int(y/TILE_SIZE)][int(x/TILE_SIZE)].setPossibleNeighbours
                # print([int(y/TILE_SIZE)], [int(x/TILE_SIZE)], GRID[int(y/TILE_SIZE)][int(x/TILE_SIZE)].neighbours)

        
    def initialize_sprites(self):
        sprite_name, index, constraints = "Sprite_", 0, SPRITESHEET_LAYOUT[self.layout_in_use]["Constraints"]
        for y in range(0, constraints["Height"], TILE_SIZE):
            for x in range(0, constraints["Width"], TILE_SIZE):
                image = self.get_sprite((x, y))
                pxarray = self.convert_pixelarray(pygame.PixelArray(image))
                if numpy.count_nonzero(pxarray) > 1:
                    self.sprites[sprite_name + str(index)] = {}
                    self.sprites[sprite_name + str(index)]["Position"] = None
                    self.sprites[sprite_name + str(index)]["Sides"] = []
                    self.sprites[sprite_name + str(index)]["Position"] = (x, y)
                    self.sprites[sprite_name + str(index)]["Sides"].append(pxarray[0])
                    self.sprites[sprite_name + str(index)]["Sides"].append([array[31] for array in pxarray])
                    self.sprites[sprite_name + str(index)]["Sides"].append(pxarray[31])
                    self.sprites[sprite_name + str(index)]["Sides"].append([array[0] for array in pxarray])
                    index += 1
    
    def get_accurate_sprite(self, current_sprite):
        matching_sides = [[] for i in range(4)] # 4 directions ( identified in Settings )
        x, y = int(current_sprite.x / TILE_SIZE), int(current_sprite.y / TILE_SIZE)
        # xSprite, ySprite = int(current_sprite.x / TILE_SIZE), int(current_sprite.y / TILE_SIZE)
        # xPrior, yPrior = int(current_sprite.prior.x / TILE_SIZE), int(current_sprite.prior.y / TILE_SIZE)
        # direction = tuple(map(operator.sub, (xSprite, ySprite), (xPrior, yPrior)))
        # direction_index = DIRECTIONS.index(direction)
        # matching_sides[direction_index] = self.sprites[current_sprite.prior.name]["Sides"][ENTROPY_DICT[direction_index]]

        if x > 0 and GRID[y][x - 1].visited:
            matching_sides[3] = self.sprites[GRID[y][x - 1].name]["Sides"][ENTROPY_DICT[3]]

        if x < (SCREEN_WIDTH / TILE_SIZE) - 1 and GRID[y][x + 1].visited:
            matching_sides[1] = self.sprites[GRID[y][x + 1].name]["Sides"][ENTROPY_DICT[1]]

        if y > 0 and GRID[y - 1][x].visited:
            matching_sides[0] = self.sprites[GRID[y - 1][x].name]["Sides"][ENTROPY_DICT[0]]

        if y < (SCREEN_HEIGHT  / TILE_SIZE) - 1 and GRID[y + 1][x].visited:
            matching_sides[2] = self.sprites[GRID[y + 1][x].name]["Sides"][ENTROPY_DICT[2]]
            
        return matching_sides
        
    def initialize_generation(self):
        # initialize grid and sprites into json array
        self.initialize_grid()
        self.initialize_sprites()
        
        # set drawing of the level to False until its ready and all sprites are generated
        self.level_ready = False
        
        # # pick a random sprite as a start
        # random_sprite = "Sprite_4"
        # start_sprite = GRID[0][0]
        # start_sprite.updateSprite(self.get_sprite(self.sprites[random_sprite]["Position"]), random_sprite)
        # self.level_sprites.add(start_sprite)
        # start_sprite.visited = True
        # start_sprite.queued = True
        # # print("x: ", int(start_sprite.x / TILE_SIZE), "y: ", int(start_sprite.y / TILE_SIZE), "Queue: ", [queue.getPosition() for queue in self.queue])
        # for neighbour in start_sprite.neighbours:
        #     # print("Neighbours: ", int(neighbour.x / TILE_SIZE), int(neighbour.y / TILE_SIZE), neighbour.queued)
        #     neighbour.queued = True
        #     neighbour.prior = start_sprite
        #     self.queue.append(neighbour)
        
        # print(GRID[0][1].prior.x, GRID[1][0].prior.x)
    
    
    def run(self, dt):
        self.display_surface.fill("black")
        if len(self.queue) > 0:
            identical = True
            possible_sprites = []
            current_sprite = self.queue.pop(0)
            current_sprite.visited = True
            # print("x: ", int(current_sprite.x / TILE_SIZE), "y: ", int(current_sprite.y / TILE_SIZE), "Queue: ", [queue.getPosition() for queue in self.queue])
            matching_sides = self.get_accurate_sprite(current_sprite)
            for key in self.sprites.keys():
                identical = True
                sides = self.sprites[key]["Sides"]
                for i in range(len(matching_sides)):
                    if len(matching_sides[i]) != 0:
                        if matching_sides[i] != sides[ENTROPY_DICT[i]]:
                            # print(matching_sides[i], sides[ENTROPY_DICT[i]], key)
                            identical = False
                                        
                if identical and key not in [current_sprite.prior.name, "Sprite_12"]: 
                    possible_sprites.append(key)
            
            print(possible_sprites)
            random_pick = random.choice(possible_sprites)
            current_sprite.updateSprite(self.get_sprite(self.sprites[random_pick]["Position"]), random_pick)
            self.level_sprites.add(current_sprite)

            for neighbour in current_sprite.neighbours:
                if not neighbour.queued:
                    neighbour.queued = True
                    neighbour.prior = current_sprite
                    self.queue.append(neighbour)     

            time.sleep(0.5)
            # self.queue = []
        
        self.level_sprites.draw(self.display_surface)
        self.level_sprites.update(dt)
    