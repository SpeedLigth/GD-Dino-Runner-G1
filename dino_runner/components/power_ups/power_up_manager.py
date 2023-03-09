import random

import pygame
from dino_runner.components.power_ups.pick_up import PickUp

from dino_runner.components.power_ups.power_up import PowerUp
from dino_runner.components.power_ups.shield import Shield


class PowerUpManager:
    def __init__(self):
        self.power_ups: list[PowerUp] = []
        self.pick_ups: list[PickUp] = []
        #En que puntaje vamos a generar el pawer_up
        self.when_appears = 0
        self.when_appears_2 = 0

    def update(self, game_speed, score, player):
        if not self.power_ups and score == self.when_appears:
            self.when_appears += random.randint(300, 500)
            self.power_ups.append(Shield())
        if not self.pick_ups and score == self.when_appears_2: 
            self.when_appears_2 += random.randint(300, 500)
            self.pick_ups.append(PickUp())

        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if power_up.rect.colliderect(player.rect):
                power_up.start_time = pygame.time.get_ticks()
                player.on_pick_power_up(power_up)
                self.power_ups.remove(power_up)
        
        for pick_up in self.pick_ups:
            pick_up.update(game_speed, self.pick_ups)
            if pick_up.rect.colliderect(player.rect):
                pick_up.start_time = pygame.time.get_ticks()
                player.on_pick_power_up(pick_up) 
                self.pick_ups.remove(pick_up)


    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)
        
        for pick_up in self.pick_ups:
            pick_up.draw(screen)

    def reset(self):
        self.power_ups = []
        self.when_appears = random.randint(300, 400)

        self.ppick_ups = []
        self.when_appears_2 = random.randint(350, 450)
