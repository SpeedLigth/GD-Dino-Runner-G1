import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.score import Score

from dino_runner.components.obstacles.obstacle_manager import ObstacleManager


from dino_runner.utils.constants import BG, DINO_START, FONT_STYLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS


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

        self.player = Dinosaur()
        self.obstacle_manage = ObstacleManager()
        self.score = Score()
        self.death_count = 0

    def run(self):
        self.executing = True
        while self.executing:
            if not self.playing:
                self.show_menu()

        pygame.quit()

    def start_game(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manage.reset()
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

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manage.draw(self.screen)
        self.score.draw(self.screen)
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

    def on_death(self):
        self.playing = False
        self.death_count += 1

    def show_menu(self):
        # Rellenar de color blanco la pantalla
        self.screen.fill((255, 255, 255))
        # Poner un mensaje de bienbenida centrado
        half_screen_width = SCREEN_WIDTH // 2
        half_screen_heigth = SCREEN_HEIGHT // 2
        if not self.death_count:
            font = pygame.font.Font(FONT_STYLE, 32)
            text = font.render("Welcome, press any key to star", True,(0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center =(half_screen_width, half_screen_heigth)
            self.screen.blit(text, text_rect)
        else:
            pass
        # Poner una imagen a modo icono en el juego
        self.screen.blit(DINO_START, (half_screen_width - 40, half_screen_heigth -140))
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
                self.start_game()
