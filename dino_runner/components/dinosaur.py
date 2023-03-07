from pygame.sprite import Sprite
import pygame

from dino_runner.utils.constants import JUMPING, RUNNING, DUCKING

DINO_RUNNING = "running"
DINO_JUMPING = "jumping"
DINO_DUCKING = "ducking"

class Dinosaur(Sprite):
    POSITION_X = 80
    POSITION_Y = 310
    JUMP_VELOCITY = 8.5

    def __init__(self):
        self.image = RUNNING[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.POSITION_X
        self.rect.y = self.POSITION_Y
        self.actions = DINO_RUNNING
        self.jump_velocity = self.JUMP_VELOCITY
        self.step = 0


    def update(self, user_input):
        if self.actions == DINO_RUNNING:
            self.run()
        elif self.actions == DINO_JUMPING:
            self.jump()
        elif self.actions == DINO_DUCKING:
            self.bend()
    
        if self.actions != DINO_JUMPING:
            if user_input[pygame.K_UP]:
                self.actions = DINO_JUMPING        
            elif user_input[pygame.K_DOWN]:
                self.actions = DINO_DUCKING
            else:
                self.actions = DINO_RUNNING

        if self.step >= 10:
            self.step = 0
 
    def jump(self):
        pos_y = self.rect.y - self.jump_velocity * 4
        self.update_image(JUMPING, pos_y=pos_y)
        self.jump_velocity -= 0.8   
        if self.jump_velocity < -self.JUMP_VELOCITY:
            self.jump_velocity = self.JUMP_VELOCITY
            self.actions = DINO_RUNNING
            self.rect.y = self.POSITION_Y

    def run(self):
        self.update_image(RUNNING[self.step // 5])
        self.step += 1
        #self.image = RUNNING[self.step // 5]
        #self.rect = self.image.get_rect()        
        #self.rect.x = self.POSITION_X
        #self.rect.y = self.POSITION_Y 
        #self.step += 1

    def bend(self):
        self.image = DUCKING[self.step // 5]  
        self.rect = self.image.get_rect()
        self.rect.x = self.POSITION_X
        self.rect.y = self.POSITION_Y+30
        self.step += 1

    def update_image(self, image: pygame.Surface, pos_x=None, pos_y=None):
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = pos_x or self.POSITION_X
        self.rect.y = pos_y or self.POSITION_Y

    def draw(self, screem):
        screem.blit(self.image, (self.rect.x, self.rect.y))
