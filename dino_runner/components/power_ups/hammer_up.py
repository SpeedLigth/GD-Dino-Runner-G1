import random
from pygame import Surface
from pygame.sprite import Sprite

from dino_runner.utils.constants import SCREEN_WIDTH

class HammerUp(Sprite):
    def __init__(self, image: Surface, type):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(900, 1500)
        self.rect.y = random.randint(300, 350)
        self.type = type
        self.duration = random.randint(5, 12) # Tiempo del power up 
        self.start_time = 0 # momento en el que
    
    def update(self, game_speed, power_ups):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            power_ups.remove(self)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
