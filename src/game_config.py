import pygame
import os

WHITE = (255, 255, 255)
FPS = 200
WIDTH = 0
HEIGHT = 0
WIN = 0

BLUE_CHARACTER = pygame.image.load(
    os.path.join("assets", "CharactersSprites1.png"))
GRAY_CHARACTER = pygame.image.load(
    os.path.join("assets", "CharactersSprites2.png"))
YELLOW_CHARACTER = pygame.image.load(
    os.path.join("assets", "CharactersSprites3.png"))

FONT = pygame.font.Font("freesansbold.ttf", 32)

class GameConfig:
    def __init__(self, number_of_agents=150,
                 number_of_days=50,
                 initial_purchase=100,
                 daily_purchase=30,
                 day_duration=100,
                 days_elapsed=0,
                 speed_limit=4,
                 sprite_width=30,
                 sprite_height=32,
                 n=638,
                 factor=1.005):
        pygame.init()
        self.number_of_agents = number_of_agents
        self.number_of_days = number_of_days
        self.initial_purchase = initial_purchase
        self.daily_purchase = daily_purchase
        self.day_duration = day_duration
        self.days_elapsed = days_elapsed
        self.speed_limit = speed_limit
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height

        # Calculate Accumulated Probability
        p = (1-factor)/(1-(factor**n))
        P = [pow(factor, i)*p for i in range(0, n)]
        self.probability = P
        self.accumulated_probability = [sum(P[:i+1]) for i in range(0, n)]

        # Day Count Text Configuration
        self.day_count_text = FONT.render(
            "Day: 0", True, (0, 255, 0), (0, 0, 255))
        self.day_count_text_container = self.day_count_text.get_rect()

gameConfig = GameConfig()
