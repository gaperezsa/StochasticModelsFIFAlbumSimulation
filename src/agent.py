import pygame
import random
import os
from global_context import context
from enum import Enum

BLUE_CHARACTER = pygame.image.load(
    os.path.join("assets", "BlueCharacter.png"))
GRAY_CHARACTER = pygame.image.load(
    os.path.join("assets", "GrayCharacter.png"))
YELLOW_CHARACTER = pygame.image.load(
    os.path.join("assets", "YellowCharacter.png"))

n = 638
factor = 1.005
p = (1-factor)/(1-(factor**n))
P = [pow(factor, i)*p for i in range(0, n)]
P_accumulated = [sum(P[:i+1]) for i in range(0, n)]
print(P_accumulated)

class AgentDirections(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'


class AgentStates(Enum):
    IDLE = 'idle'
    TRADING = 'trading'


class Agent:
    def __init__(self, initial_x, initial_y, aficionado_number, simulation_config):
        self.config = simulation_config
        # Positions of the agent
        self.x = initial_x
        self.y = initial_y
        # Speed of the agent
        self.x_speed = 0
        self.y_speed = 0
        # Stickers of the agent
        self.obtained = set()
        self.repeated = []
        self.filled = False
        # Open envelopes
        self.envelopes_opened = 0
        self.stickers_traded = 0
        self.previous_inertial_frame = [0, 0, 30, 32]
        self.current_direction = AgentDirections.DOWN
        self.character = BLUE_CHARACTER
        if aficionado_number == 0:
            self.character = BLUE_CHARACTER
        elif aficionado_number == 1:
            self.character = GRAY_CHARACTER
        elif aficionado_number == 2:
            self.character = YELLOW_CHARACTER
        self.state = AgentStates.IDLE  # idle,trading
        self.frames_to_finish_trade = 0
        self.last_traded_with = -1

    def get_rectangle(self):
        config = self.config
        return pygame.Rect(self.x, self.y, config.sprite_width, config.sprite_height)

    def next_random_move(self):
        config = self.config
        if self.state == AgentStates.TRADING:
            return

        self.x_speed += random.uniform(-1, 1)
        self.y_speed += random.uniform(-1, 1)
        self.x_speed = config.speed_limit if self.x_speed > config.speed_limit else self.x_speed
        self.x_speed = -config.speed_limit if self.x_speed < - \
            config.speed_limit else self.x_speed
        self.y_speed = config.speed_limit if self.y_speed > config.speed_limit else self.y_speed
        self.y_speed = -config.speed_limit if self.y_speed < - \
            config.speed_limit else self.y_speed

        if self.x + self.x_speed < 0:
            self.x_speed = config.speed_limit
        elif self.x + self.x_speed > context.width:
            self.x_speed = -config.speed_limit
        self.x += self.x_speed

        if self.y + self.y_speed < 0:
            self.y_speed = config.speed_limit
        elif self.y + self.y_speed > context.height:
            self.y_speed = -config.speed_limit
        self.y += self.y_speed

    def get_repeated(self):
        return self.repeated

    def add_sticker(self, sticker):
        self.obtained.add(sticker)

    def is_filled(self):
        return self.filled

    def open_envelope(self):
        def get_random_sticker():
            rand = random.uniform(0, 1)
            for p in P_accumulated:
                if rand <= p:
                    sticker = P_accumulated.index(p)
                    return sticker
            return n-1
        if self.is_filled():
            return
        for i in range(0, 5):
            sticker = get_random_sticker()
            assert sticker != None
            if sticker in self.obtained:
                self.repeated.append(sticker)
            else:
                self.obtained.add(sticker)
                # Check if album is filled
                self.check_album_filled()
        # Add the opened envelope
        self.envelopes_opened += 1

    def remove_repeated(self, sticker):
        self.repeated.remove(sticker)

    def count_sticker_traded(self):
        self.stickers_traded += 1

    def get_envelopes_opened(self):
        opened = self.envelopes_opened + (self.stickers_traded / 5)
        return opened

    def trade(self, trader):
        def calculate_price(stickers):
            return sum([1/P[sticker] for sticker in stickers])

        if self.is_filled() or trader.is_filled():
            return

        trader_repeated = trader.get_repeated()
        self_missing = []
        trader_missing = []
        # Check stickers self_missing that are available in repeated list of peer
        for sticker in trader_repeated:
            if sticker not in self.obtained:
                self_missing.append(sticker)
        # Check stickers self_missing for peer that are available in my repeated list
        for sticker in self.repeated:
            if sticker not in trader.obtained:
                trader_missing.append(sticker)
        # No trade if someone does not have any sticker on the lists
        if len(self_missing) == 0 or len(trader_missing) == 0:
            return
        # sort lists
        self_missing.sort()
        trader_missing.sort()
        # CalculatePrice and make deal
        self_price = calculate_price(trader_missing)
        trader_price = calculate_price(self_missing)
        delta = self_price - trader_price
        if delta > 0:
            while delta > 0:
                most_valuable_sticker = trader_missing.pop(-1)
                self_price = calculate_price(trader_missing)
                trader_price = calculate_price(self_missing)
                delta = self_price - trader_price
            trader_missing.append(most_valuable_sticker)
        elif delta < 0:
            while delta < 0:
                most_valuable_sticker = self_missing.pop(-1)
                self_price = calculate_price(trader_missing)
                trader_price = calculate_price(self_missing)
                delta = self_price - trader_price
            self_missing.append(most_valuable_sticker)

        # Make deal and add the sticker to total stickers traded
        for sticker in self_missing:
            self.add_sticker(sticker)
            trader.remove_repeated(sticker)
            self.count_sticker_traded()
        for sticker in trader_missing:
            trader.add_sticker(sticker)
            self.remove_repeated(sticker)
            trader.count_sticker_traded()

        # Check if album is already filled
        self.check_album_filled()
        trader.check_album_filled()

    def check_album_filled(self):
        if len(self.obtained) == n:
            self.filled = True

    def next_intertial_frame(self):
        config = self.config
        epsilon = 0.01
        if abs(self.x_speed) < 0+epsilon and abs(self.x_speed) < 0+epsilon:
            self.previous_inertial_frame[0] = 30
        elif abs(self.x_speed) > abs(self.y_speed):
            if self.x_speed < 0 and self.current_direction == AgentDirections.LEFT:
                self.previous_inertial_frame[0] = (
                    self.previous_inertial_frame[0] + config.sprite_width) % (3*config.sprite_width)
            elif self.x_speed < 0 and self.current_direction != AgentDirections.LEFT:
                self.previous_inertial_frame[0] = 0
                self.previous_inertial_frame[1] = config.sprite_height
                self.current_direction = AgentDirections.LEFT
            elif self.x_speed > 0 and self.current_direction == AgentDirections.RIGHT:
                self.previous_inertial_frame[0] = (
                    self.previous_inertial_frame[0] + config.sprite_width) % (3*config.sprite_width)
            elif self.x_speed > 0 and self.current_direction != AgentDirections.RIGHT:
                self.previous_inertial_frame[0] = 0
                self.previous_inertial_frame[1] = 2*config.sprite_height
                self.current_direction = AgentDirections.RIGHT
        elif abs(self.y_speed) > abs(self.x_speed):
            if self.y_speed < 0 and self.current_direction == AgentDirections.UP:
                self.previous_inertial_frame[0] = (
                    self.previous_inertial_frame[0] + config.sprite_width) % (3*config.sprite_width)
            elif self.y_speed < 0 and self.current_direction != AgentDirections.UP:
                self.previous_inertial_frame[0] = 0
                self.previous_inertial_frame[1] = 3*config.sprite_height
                self.current_direction = AgentDirections.UP
            elif self.y_speed > 0 and self.current_direction == AgentDirections.DOWN:
                self.previous_inertial_frame[0] = (
                    self.previous_inertial_frame[0] + 30) % 90
            elif self.y_speed > 0 and self.current_direction != AgentDirections.DOWN:
                self.previous_inertial_frame[0] = 0
                self.previous_inertial_frame[1] = 0
                self.current_direction = AgentDirections.DOWN

        if self.state == AgentStates.TRADING:
            self.previous_inertial_frame[0] = 30

        return self.previous_inertial_frame
