from Entities.Tile import Tile
from Settings import SCREEN_HEIGHT, SCREEN_WIDTH
import random
from Entities.Items import *

class Room:
    def __init__(self, index, level=None):
        self.index = index
        self.width, self.height = ROOM_WIDTH, ROOM_HEIGHT
        self.level = level
        self.collapsed = False
        self.room_type = None
        self.currentX, self.currentY = 0, 0
        self.room_tiles = []
        self.items_positions = []
        self.max_items = 5
        self.big_map = Big_Map(30, 31, 1 * SCALE_SIZE, 4 * SCALE_SIZE)
            
    def set_level(self, items, level, tiles, tiles_collision, SPRITES, room_type, i, j, has_item):
        self.level = level
        self.collapsed = True
        self.room_type = room_type
        self.position = (i * self.width, j * self.height)
        self.trigger_draw(tiles, tiles_collision, SPRITES)
        if self.index in has_item:
            items.append(self.big_map)

    def trigger_draw(self, tiles, tiles_collision, SPRITES):
        for x in range(len(self.level.collide_layer)):
            tile_index = self.level.collide_layer[x] - 1
            tile = Tile(self.currentX, self.currentY, self.position, SPRITES[tile_index])
            if (tile_index <= 174 or tile_index in [420, 421, 422, 423, 455, 456, 457, 458]) and tile_index != 36 :
                tile.set_colision(True)
                tiles_collision.add(tile)
            tiles.add(tile); self.room_tiles.append(tile)
            self.currentX += 1
            if self.currentX >= self.level.room_width:
                self.currentY += 1
                self.currentX = 0
            