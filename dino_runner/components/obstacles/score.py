import pygame
from dino_runner.utils.constants import FONT_STYLE, POINTS


class Score:
    def __init__(self):
        self.score = 0

    def update(self, game):
        self.score += 1
        if self.score % 100 == 0:
            game.game_speed += 2
        
    
    def draw(self, screen):
        font = pygame.font.Font(FONT_STYLE, 24)
        text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (950, 30)
        screen.blit(text, text_rect)
    
    def get_score(self):
        return self.score
    
    def get_max_point(self):
        max = POINTS[0]
        for p in range(len(POINTS)):
            if POINTS[p] > max:
                max = POINTS[p]
        return max
    
    def reset(self):
        self.score = 0
