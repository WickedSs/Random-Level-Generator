from pygame.math import Vector2
import sys, os, pygame, numpy, random, time, string
from Settings import *
import operator
from itertools import chain


alphabet = string.ascii_letters
ROOT = os.path.dirname(sys.modules['__main__'].__file__)
GRID = []
VISITED = []

class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x, self.y, index = x, y, None
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(random.choice(["green", "black", "red"]))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.queued = False
        self.visited = False
        self.neighbours, self.next_sprites = [], {0 : [], 1 : [], 2 : [], 3 : []}

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
    
    def updateSprite(self, image, index):
        self.image = image
        self.index = index

    def getPosition(self):
        return (int(self.x/TILE_SIZE), int(self.y/TILE_SIZE))
    


class Level:
    spritesheet_filename = os.path.join(ROOT, "Assets/Spritesheet.png")
    example_file_01 = os.path.join(ROOT, "Assets\Example-01.png")
    def __init__(self):
        # self.sprite_sheet = pygame.image.load(self.spritesheet_filename).convert_alpha()
        self.sprite_sheet = pygame.image.load(self.example_file_01).convert_alpha()
        self.sprite_sheet_rect = self.sprite_sheet.get_rect()
        self.display_surface = pygame.display.get_surface()
        self.level_sprites = pygame.sprite.Group()
        self.queue, self.sprites = [], [[None for j in range(15)] for i in range(9)]
        self.layout_in_use = "First_Layout"
        self.initialize_generation()
        

    def get_sprite(self, position):
        x, y = position
        sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, TILE_SIZE, TILE_SIZE))
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

    def get_sprite_neighbours(self, x, y, array):
        x, y, neighbours = int(x / TILE_SIZE), int(y / TILE_SIZE), array
        if x > 0:
            working_x, working_y = x - 1, y
            neighbours[3].append((working_x, working_y))
        
        if x < (self.sprite_sheet_rect.width / TILE_SIZE) - 1:
            working_x, working_y = x + 1, y
            neighbours[1].append((working_x, working_y))
        
        if y > 0:
            working_x, working_y = x, (y - 1) 
            neighbours[0].append((working_x, working_y))

        if y < (self.sprite_sheet_rect.height  / TILE_SIZE) - 1:
            working_x, working_y = x, (y + 1)
            neighbours[2].append((working_x, working_y))
        
        return neighbours
    
    def initialize_sprites(self):
        sprite_name, index, already_added = "Sprite_", 0, [[None for j in range(15)] for i in range(9)]
        for y in range(0, self.sprite_sheet_rect.height, TILE_SIZE):
            for x in range(0, self.sprite_sheet_rect.width, TILE_SIZE):
                image = self.get_sprite((x, y))
                pxarray = self.convert_pixelarray(pygame.PixelArray(image))
                if pxarray not in chain(*already_added):
                    self.sprites[int(y/TILE_SIZE)][int(x/TILE_SIZE)] = [sprite_name + str(index), (x, y) , { 0 : [], 1 : [], 2 : [], 3 : [] } ]
                    neighbours = self.get_sprite_neighbours(x, y, self.sprites[int(y/TILE_SIZE)][int(x/TILE_SIZE)][2])
                    self.sprites[int(y/TILE_SIZE)][int(x/TILE_SIZE)][2] = neighbours
                    already_added[int(y/TILE_SIZE)][int(x/TILE_SIZE)] = pxarray
                    # print(sprite_name + str(index), self.sprites[sprite_name + str(index)]["Info"]["Coords"], self.sprites[sprite_name + str(index)]["Sides"])
                    index += 1
                else:
                    index_row = [already_added.index(row) for row in already_added if pxarray in row][0]
                    index_column = [row.index(pxarray) for row in already_added if pxarray in row][0]
                    self.sprites[index_row][index_column][2] = self.get_sprite_neighbours(x, y, self.sprites[index_row][index_column][2])
        
        
    
    def get_accurate_sprite(self, current_sprite):
        neighbours_found = [None for i in range(4)] # 4 directions ( identified in Settings )
        x, y = int(current_sprite.x / TILE_SIZE), int(current_sprite.y / TILE_SIZE)

        if x > 0 and GRID[y][x - 1].visited:
            neighbours_found[3] = GRID[y][x - 1]

        if x < (SCREEN_WIDTH / TILE_SIZE) - 1 and GRID[y][x + 1].visited:
            neighbours_found[1] = GRID[y][x + 1]

        if y > 0 and GRID[y - 1][x].visited:
            neighbours_found[0] = GRID[y - 1][x]

        if y < (SCREEN_HEIGHT  / TILE_SIZE) - 1 and GRID[y + 1][x].visited:
            neighbours_found[2] = GRID[y + 1][x]
            
        return neighbours_found
        
    def initialize_generation(self):
        # initialize grid and sprites into json array
        self.initialize_grid()
        self.initialize_sprites()
        
        # set drawing of the level to False until its ready and all sprites are generated
        self.level_ready = False
        
        # pick a random sprite as a start
        random_sprite = random.choice(list(self.sprites.keys()))
        index = list(self.sprites.keys()).index(random_sprite)
        start_sprite = GRID[random.randrange(0, (SCREEN_HEIGHT / TILE_SIZE))][random.randrange(0, (SCREEN_WIDTH / TILE_SIZE))]
        start_sprite.updateSprite(self.get_sprite(self.sprites[random_sprite]["Info"]["Coords"]), index)
        self.level_sprites.add(start_sprite)
        start_sprite.visited = True
        start_sprite.queued = True
        for neighbour in start_sprite.neighbours:
            neighbour.queued = True
            self.queue.append(neighbour)
        
        print("Queue: ", len(self.queue))

    def run(self, dt):
        self.display_surface.fill("black")
        if len(self.queue) > 0:
            possible_sprites = []
            current_sprite = self.queue.pop(0)
            current_sprite.visited = True
            neighbours_found = self.get_accurate_sprite(current_sprite)
            for neighbour_exist in neighbours_found:
                if neighbour_exist:
                    possible_sprites.extend(self.sprites["Sprite_" + str(neighbour_exist.index)]["Sides"][ENTROPY_DICT[neighbours_found.index(neighbour_exist)]])
            
            print("Queue: ", len(self.queue))
            if len(possible_sprites) > 0:
                random_pick = random.choice(possible_sprites)
                random_pick = tuple(map(operator.mul, random_pick, (TILE_SIZE, TILE_SIZE)))
                selected_sprite = [sprite for sprite in list(self.sprites.keys()) if self.sprites[sprite]["Info"]["Coords"] == random_pick]
                picked = random.choice(selected_sprite) if len(selected_sprite) > 1 else selected_sprite[0] if len(selected_sprite) == 1 else None
                current_sprite.updateSprite(self.get_sprite(self.sprites[picked]["Info"]["Coords"]), list(self.sprites.keys()).index(picked))
                self.level_sprites.add(current_sprite)

                for neighbour in current_sprite.neighbours:
                    if not neighbour.queued:
                        neighbour.queued = True
                        self.queue.append(neighbour)     

            time.sleep(0.5)
            # self.queue = []
        
        self.level_sprites.draw(self.display_surface)
        self.level_sprites.update(dt)
    