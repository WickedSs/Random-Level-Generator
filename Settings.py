from turtle import width
from pygame.math import Vector2


FPS = 60
SCREEN_WIDTH = 64 * 15 #1440
SCREEN_HEIGHT = 64 * 9 #768
TILE_SIZE = 32
SCALE_SIZE = TILE_SIZE * 2
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)] # (x, y) UP, RIGHT, DOWN, LEFT
ENTROPY_DICT = { 0 : 2, 1 : 3, 2 : 0, 3 : 1}
GAME_LAYERS = ["LEVEL", "DECORATION"]
SPRITESHEET_LAYOUT = {
    "First_Layout": {
        "Constraints" : {
            "Width" : 544,
            "Height" : 352
        },
        "Collide" : {
            "From" : (0, 0),
            "To" : (512, 128),
            "Interact" : True
        },
        "Decoration" : {
            "From" : (0, 192),
            "To" : (512, 320),
            "Interact" : False
        }
    },
    "Second_Layout" : {
        "Constraints" : (),
        "Collide" : {
            "From" : (0, 0),
            "To" : ()
        },
        "Decoration" : {
            "From": (),
            "To" : ()
        }
    }
}
