import os, sys, pygame
from Entities.Item import Item



ROOT = os.path.dirname(sys.modules['__main__'].__file__)
PARTICLES_FOLDER = "Assets\Particles"


class Particle:
    def __init__(self):
        pass


class Big_Map_particle(Item):
    def __init__(self, status, width, height):
        super().__init__(width, height, 0, 0)
        self.display_surface = pygame.display.get_surface()
        self.asset_name = "Map_Effect"
        self.animation_type = "Multiple"
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.animations = {}
        self.animation_index = 0
        self.status = status
        self.path = os.path.join(PARTICLES_FOLDER, self.asset_name)
        self.status_path = os.path.join(self.path, self.status)
        self.multiple_animations()
        self.working_animation = self.animations[status]
        
    def play_animation_once(self):
        self.animation_index += 0.12
        if self.animation_index >= len(self.working_animation):
            self.animation_index = 0
            print("Ended")
            return True
        
        self.get_frame(True, 30, 31)
        self.update(0, 0)
        self.draw()
        return False
        

class Particles:
    def __init__(self, character):
        self.character = character
        self.particles = {}
        self.particle_folders = []
        self.load_particles()


    def load_particles(self):
        particles_path = os.path.join(PARTICLES_FOLDER, self.character)
        for folder in os.listdir(particles_path):
            self.particles[folder] = {}
            self.particles[folder]["frames"] = []
            frames_path = os.path.join(PARTICLES_FOLDER, self.character, folder)
            self.particle_folders.append(folder)
            for frame in os.listdir(frames_path):
                if os.path.isfile(os.path.join(frames_path, frame)):
                    self.particles[folder]["frames"].append(frame)