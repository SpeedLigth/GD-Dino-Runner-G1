import random
import pygame
from dino_runner.components.obstacles.birds import Birds
from dino_runner.components.obstacles.cactus import Cactus

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game_speed, player, game):
        if random.randint(0, 7) >= 5:
            if not self.obstacles:
                self.obstacles.append(Cactus())
        elif not self.obstacles:
            self.obstacles.append(Birds())


        for obstacle in self.obstacles:
            obstacle.update(game_speed, self.obstacles)
            if player.rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                game.playing = False

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)