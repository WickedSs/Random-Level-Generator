import os, sys, pygame
from Entities.Item import Item


ROOT = os.path.dirname(sys.modules['__main__'].__file__)
DECORATIONS_FOLDER = "Assets\Decorations"



class Cannon:
    def __init__(self):
        pass


class Candle:
    def __init__(self):
        pass
    

class Chains:
    def __init__(self, x, y):
        pass

class Door(Item):
    def __init__(self, width, height, animate, scale, x, y):
        super().__init__(width, height, animate, scale, x, y)
        self.asset_name = "Door"
        self.animation_type = "Multiple"
        self.animations = {}
        self.animation_index = 0
        self.status = "Opening"
        self.open, self.action, self.played = False, False, 0
        self.path = os.path.join(DECORATIONS_FOLDER, self.asset_name)
        self.multiple_animations()
        self.working_animation = self.animations[self.status]
        self.get_frame()

    def on_collision(self, player, items_list):
        if player.rect.colliderect(self.rect) and not self.open:
            action = player.trigger_floating_text("[E]", self.rect.x + self.rect.w / 4, self.rect.y - (self.rect.h / 4))
            if action:
                self.working_animation = self.animations[self.status]
                self.open = True
           
                
        if self.open and not self.action and self.played == 0:
            status = self.play_animation_once()
            if status:
                player.overlay.dim_screen_bool = status
                self.open, self.action, self.played = False, False, 1
                
    def play_animation_once(self):
        self.animation_index += 0.12
        if self.animation_index >= len(self.working_animation):
            self.animation_index = 0
            return True
        
        self.get_frame()
        self.display_surface.blit(self.image, self.rect)
        return False

class Window:
    def __init__(self):
        pass

    
class Barrel_UP:
    def __init__(self):
        pass


class Barrel_Down:
    def __init__(self):
        pass
    

class Bottle_UP_1:
    def __init__(self):
        pass
    

class Bottle_UP_2:
    def __init__(self):
        pass
    

class Bottle_Down_1:
    def __init__(self):
        pass
    

class Bottle_Down_2:
    def __init__(self):
        pass