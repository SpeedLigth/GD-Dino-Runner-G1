import random
from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD

class Birds(Obstacle):

    def __init__(self):
        image = BIRD
        type = 0
        super().__init__(image, type)
        y = [320, 270, 200]
        self.rect.y = random.choice(y)
        self.step = 0

    def draw(self, screem):
        if self.step >= 10:
            self.step = 0
        screem.blit(self.image[self.step // 5], (self.rect.x, self.rect.y))
        self.step += 1