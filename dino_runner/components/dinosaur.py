from pygame.sprite import Sprite
import pygame

from dino_runner.utils.constants import DEFAULT_TYPE, DUCKING_SHIELD, JUMPING, JUMPING_SHIELD, RUNNING, DUCKING, RUNNING_SHIELD, SHIELD_TYPE

DINO_RUNNING = "running"
DINO_JUMPING = "jumping"
DINO_DUCKING = "ducking"

DUCK_IMG = {DEFAULT_TYPE : DUCKING, SHIELD_TYPE: DUCKING_SHIELD}
JUMP_IMG = {DEFAULT_TYPE : JUMPING, SHIELD_TYPE: JUMPING_SHIELD}
RUN_IMG = {DEFAULT_TYPE : RUNNING, SHIELD_TYPE: RUNNING_SHIELD}

class Dinosaur(Sprite):
    POSITION_X = 80
    POSITION_Y = 310
    JUMP_VELOCITY = 8.5

    def __init__(self):
        self.type = DEFAULT_TYPE
        self.power_up_time_up = 0
        self.image = (RUN_IMG[self.type][0])
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
        self.update_image(JUMP_IMG[self.type], pos_y=pos_y)
        self.jump_velocity -= 0.8   
        if self.jump_velocity < -self.JUMP_VELOCITY:
            self.jump_velocity = self.JUMP_VELOCITY
            self.actions = DINO_RUNNING
            self.rect.y = self.POSITION_Y

    def run(self):
        self.update_image(RUN_IMG[self.type][self.step // 5])
        self.step += 1
        #self.image = RUNNING[self.step // 5]
        #self.rect = self.image.get_rect()        
        #self.rect.x = self.POSITION_X
        #self.rect.y = self.POSITION_Y 
        #self.step += 1

    def bend(self):
        self.image = (DUCK_IMG[self.type][self.step // 5])  
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

    def on_pick_power_up(self, power_up):
        self.type = power_up.type
        self.power_up_time_up = power_up.start_time + (power_up.duration * 1000)
    
    def check_power_up(self, screen):
        if self.type == SHIELD_TYPE:
            time_to_show = round((self.power_up_time_up - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                print(f"{self.type.capitalize()} enabled for {time_to_show} seconds,", screen,) #(font_size=16, pos_y_center=50))
            else:
                self.type = DEFAULT_TYPE
                self.power_up_time_up = 0