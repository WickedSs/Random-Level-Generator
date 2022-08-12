from itertools import count
import queue
from tracemalloc import start
from typing import NewType
from pygame.math import Vector2
import sys, os, pygame, numpy, random
from Settings import *
import operator



ROOT = os.path.dirname(sys.modules['__main__'].__file__)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.x, self.y = x, y
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.setNeighbours()

    def setNeighbours(self):
        for direction in DIRECTIONS:
            new_tuple = tuple(map(operator.add, (self.x, self.y), direction))
            if new_tuple[0] >= 0 and new_tuple[0] < SCREEN_WIDTH and new_tuple[1] >= 0 and new_tuple[1] < SCREEN_HEIGHT:
                self.neighbours.append(new_tuple)
            
    def updateSprite(self, image, name):
        self.name = name
        self.image = image
        self.rect = pygame.Rect((self.x, self.y), (TILE_SIZE, TILE_SIZE))
    


class Level:
    spritesheet_filename = os.path.join(ROOT, "Assets/Spritesheet.png")
    def __init__(self):
        self.sprite_sheet = pygame.image.load(self.spritesheet_filename).convert_alpha()
        self.display_surface = pygame.display.get_surface()
        self.level_sprites = pygame.sprite.Group()
        self.grid, self.queue = [], []
        self.sprites = {}

    def get_sprite(self, position):
        sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet, (0, 0), (position[0], position[1], TILE_SIZE, TILE_SIZE))
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
    
    def initialize_grid_and_sprites(self):
        sprite_name, index = "Sprite_", 0
        for y in range(0, self.sprite_sheet.get_rect().h, TILE_SIZE):
            self.grid.append([])
            for x in range(0, self.sprite_sheet.get_rect().w, TILE_SIZE):
                self.grid[int(y/TILE_SIZE)].append(Sprite(self.level_sprites, int(x/TILE_SIZE), int(y/TILE_SIZE)))
                image = self.get_sprite(x, y)
                pxarray = self.convert_pixelarray(pygame.PixelArray(image))
                if numpy.count_nonzero(pxarray) > 1:
                    self.sprites[sprite_name + str(index)] = {}
                    self.sprites[sprite_name + str(index)]["Position"] = None
                    self.sprites[sprite_name + str(index)]["Sides"] = {}
                    self.sprites[sprite_name + str(index)]["Position"] = (x, y)
                    self.sprites[sprite_name + str(index)]["Sides"][0] = pxarray[0]
                    self.sprites[sprite_name + str(index)]["Sides"][1] = [array[0] for array in pxarray]
                    self.sprites[sprite_name + str(index)]["Sides"][2] = pxarray[31]
                    self.sprites[sprite_name + str(index)]["Sides"][3] = [array[31] for array in pxarray]
                    index += 1
    
    def get_accurate_sprite(self):
        neighbors_found = [[] for i in range(4)] # 4 directions ( identified in Settings )
        for direction in DIRECTIONS:
            x, y = tuple(map(operator.add, (self.x, self.y), direction))
            if self.grid[x][y].visited:
                neighbors_found[DIRECTIONS.index(direction)] = self.sprites[self.grid[x][y].name]["Sides"][ENTROPY_DICT[DIRECTIONS.index(direction)]]
        return neighbors_found
        
    def generate_level(self):
        # initialize grid and sprites into json array
        self.initialize_grid_and_sprites()
        
        # set drawing of the level to False until its ready and all sprites are generated
        self.level_ready = False
        
        # pick a random sprite as the start
        random_sprite = random.choice(list(self.sprites.keys()))
        start_sprite = self.grid[0][0]
        start_sprite.setImage(self.get_sprite(self.sprites[random_sprite]["Position"]), random_sprite)
        start_sprite.visited = True
        self.queue.append(start_sprite)
        while len(self.queue) > 0:
            current_sprite = self.queue.pop(0)
            current_sprite.visited = True
            self.queue.extend(current_sprite.neighbours)
            if current_sprite.x == len(self.grid) - 1 and current_sprite.y == len(self.grid[0]) - 1:
                break
            else:
                break
        
        self.level_ready = True
    
    def run(self, dt):
        self.generate_map()
        self.display_surface.fill("black")
        if (self.map_ready):
            self.level_sprites.draw(self.display_surface)
        self.level_sprites.update(dt)
        self.level_sprites.empty()
    