from logging import Manager
import random
import pygame

from dino_runner.components.dinosaur import Dinosaur
# from dino_runner.components.obstacles.cloud import Cloud
from dino_runner.components.obstacles.score import Score

from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager


from dino_runner.utils.constants import BG, CLOUD, DINO_START, FONT_STYLE, GAME_OVER, HAMMER_TYPE, ICON, MESSAGES, POINTS, SCREEN_HEIGHT, SCREEN_WIDTH, SHIELD_TYPE, TITLE, FPS


class Game:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.executing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.x_pos_cloud = 0
        self.y_pos_clouds= 90
        self.message = MESSAGES

        self.half_screen_width = SCREEN_WIDTH // 2
        self.half_screen_heigth = SCREEN_HEIGHT // 2

        self.player = Dinosaur()
        self.obstacle_manage = ObstacleManager()
        self.score = Score()
        self._score = None
        self.death_count = 0
        self.power_up_manager = PowerUpManager()
    def run(self):
        self.executing = True
        while self.executing:
            if not self.playing:
                self.show_menu()
        pygame.quit()

    def start_game(self):
        # Game loop: events - update - draw
        self.message = MESSAGES[random.randint(1, len(MESSAGES)-1)]
        self.playing = True
        self.obstacle_manage.reset()
        self.score.reset()
        self.power_up_manager.reset()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manage.update(self.game_speed, self.player, self.on_death)
        self.score.update(self)
        self.power_up_manager.update(self.game_speed, self.score.score, self.player)
        # self.cloud.update()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.draw_cloud()
        self.player.draw(self.screen)
        self.obstacle_manage.draw(self.screen)
        self.score.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.player.check_power_up(self.screen)
        # pygame.display.update()
        pygame.display.flip() 

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
    
    
    def draw_cloud(self):
        self.screen.blit(CLOUD, (self.x_pos_cloud, self.y_pos_clouds))
        self.screen.blit(CLOUD, (SCREEN_WIDTH-100 + self.x_pos_cloud, self.y_pos_clouds))
        if self.x_pos_cloud <= -SCREEN_WIDTH:
            self.screen.blit(CLOUD, (SCREEN_WIDTH + self.x_pos_cloud, self.y_pos_clouds))
            self.x_pos_cloud = 0
        self.x_pos_cloud -= self.game_speed

    def on_death(self):
        is_invincible = self.player.type == SHIELD_TYPE
        pick = self.player.type == HAMMER_TYPE
        if not is_invincible and  not pick:
            pygame.time.delay(500)
            self.playing = False
            self.death_count += 1

    def show_menu(self):
        # Rellenar de color blanco la pantalla
        self.screen.fill((255, 255, 255))
        # Poner un mensaje de bienbenida centrado
        self.screen.blit(DINO_START, (self.half_screen_width - 40, self.half_screen_heigth -140))
        font = pygame.font.Font(FONT_STYLE, 32)
        
        if not self.death_count:
            text = font.render(MESSAGES[0], True,(0, 0, 0))
            _score = font.render("Score: "+ str(0) +"  -  "+ str(0) , True,(0, 0, 255))
            death = font.render("", True,(0, 0, 0))
        else:
            self.screen.blit(GAME_OVER, (self.half_screen_width- 190, self.half_screen_heigth -190))
            font = pygame.font.Font(FONT_STYLE, 32)
            text = font.render(self.message , True,(0, 0, 0))
            _score = font.render("Score: "+ str(self.score.get_max_point()) +"  -  "+ str(self.score.get_score()) , True,(0, 0, 255))
            death = font.render("Death: "+ str(self.death_count) , True,(255, 0, 0))

        text_rect = text.get_rect()
        text_rect.center = (self.half_screen_width, self.half_screen_heigth)
        self.screen.blit(text, text_rect)

        text_rect_score = _score.get_rect()
        text_rect_score.center = (self.half_screen_width-400, self.half_screen_heigth+230)
        self.screen.blit(_score, text_rect_score)

        text_rect_death = death.get_rect()
        text_rect_death.center = (self.half_screen_width, self.half_screen_heigth+50)
        self.screen.blit(death, text_rect_death)



        # PLasmar los cambios
        pygame.display.update()
        # Manejar eventos
        self.handle_menu_events()

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.executing = False
            elif event.type == pygame.KEYDOWN:
                POINTS.append(self.score.get_score())
                self.score = Score()
                self.start_game()

    