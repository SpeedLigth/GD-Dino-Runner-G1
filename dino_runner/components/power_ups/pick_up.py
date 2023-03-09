from dino_runner.components.power_ups.hammer_up import HammerUp
from dino_runner.utils.constants import HAMMER, HAMMER_TYPE


class PickUp(HammerUp):
    def __init__(self):
        super().__init__(HAMMER, HAMMER_TYPE)