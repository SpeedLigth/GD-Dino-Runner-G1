
import random
from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD

class Birds(Obstacle):

    def __init__(self):
        self.step = 0
        image = BIRD[self.step//5]
        self.step += 1
        super().__init__(image)
        self.rect.y = 270