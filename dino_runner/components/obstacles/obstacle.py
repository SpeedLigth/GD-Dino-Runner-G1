from pygame import Surface
from pygame.sprite import Sprite

from dino_runner.utils.constants import SCREEN_WIDTH

class Obstacle(Sprite):
    def __init__(self, image:Surface, type):
        self.image = image
        self.type = type
        if self.type == 0:
            self.rect = self.image[0].get_rect()
        else:
            self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
    
    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.remove(self)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

