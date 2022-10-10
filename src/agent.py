import pygame
import random
from game_config import gameConfig, BLUE_CHARACTER, GRAY_CHARACTER, YELLOW_CHARACTER, WIDTH, HEIGHT

class Agent:
    def __init__(self, initialX, initialY, aficionado_number):
        # Positions of the agent
        self.x = initialX
        self.y = initialY
        # Speed of the agent
        self.x_speed = 0
        self.y_speed = 0
        # Stickers of the agent
        self.obtained = set()
        self.repeated = []
        self.filled = False
        # Open envelopes
        self.envelopesOpened = 0
        self.stickersTraded = 0
        self.previous_inertial_frame = [0, 0, 30, 32]
        self.current_direction = "down"
        self.aficionado_image = BLUE_CHARACTER
        if aficionado_number == 0:
            self.aficionado_image = BLUE_CHARACTER
        elif aficionado_number == 1:
            self.aficionado_image = GRAY_CHARACTER
        elif aficionado_number == 2:
            self.aficionado_image = YELLOW_CHARACTER
        self.state = "idle"  # idle,trading
        self.frames_to_finish_trade = 0
        self.last_traded_with = -1

    def get_rectangle(self):
        return pygame.Rect(self.x, self.y, gameConfig.sprite_width, gameConfig.sprite_height)

    def next_random_move(self):
        if self.state == "trading":
            return
        speed_limit = gameConfig.speed_limit
        self.x_speed += random.uniform(-1, 1)
        self.y_speed += random.uniform(-1, 1)
        self.x_speed = speed_limit if self.x_speed > speed_limit else self.x_speed
        self.x_speed = -speed_limit if self.x_speed < -speed_limit else self.x_speed
        self.y_speed = speed_limit if self.y_speed > speed_limit else self.y_speed
        self.y_speed = -speed_limit if self.y_speed < -speed_limit else self.y_speed

        if self.x + self.x_speed < 0:
            self.x_speed = speed_limit
        elif self.x + self.x_speed > WIDTH:
            self.x_speed = -speed_limit
        self.x += self.x_speed

        if self.y + self.y_speed < 0:
            self.y_speed = speed_limit
        elif self.y + self.y_speed > HEIGHT:
            self.y_speed = -speed_limit
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
            accumulated_probability = gameConfig.accumulated_probability
            for p in accumulated_probability:
                if rand <= p:
                    sticker = accumulated_probability.index(p)
                    return sticker
            return gameConfig.n-1
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
        self.envelopesOpened += 1

    def remove_repeated(self, sticker):
        self.repeated.remove(sticker)

    def count_sticker_traded(self):
        self.stickersTraded += 1

    def get_envelopes_opened(self):
        opened = self.envelopesOpened + (self.stickersTraded / 5)
        return opened

    def trade(self, otherAgent):
        def calculatePrice(stickers):
            return sum([1/gameConfig.probability[sticker] for sticker in stickers])

        if self.is_filled() or otherAgent.is_filled():
            return

        myRepeated = self.repeated
        peerRepeated = otherAgent.get_repeated()
        needed = []
        PeersNeeds = []
        # Check stickers needed that are available in repeated list of peer
        for sticker in peerRepeated:
            if sticker not in self.obtained:
                needed.append(sticker)
        # Check stickers needed for peer that are available in my repeated list
        for sticker in myRepeated:
            if sticker not in otherAgent.obtained:
                PeersNeeds.append(sticker)
        # No trade if someone does not have any sticker on the lists
        if len(needed) == 0 or len(PeersNeeds) == 0:
            return
        # sort lists
        needed.sort()
        PeersNeeds.sort()
        # CalculatePrice and make deal
        myPrice = calculatePrice(PeersNeeds)
        peerPrice = calculatePrice(needed)
        delta = myPrice - peerPrice
        if delta > 0:
            while delta > 0:
                mostValueSticker = PeersNeeds.pop(-1)
                myPrice = calculatePrice(PeersNeeds)
                peerPrice = calculatePrice(needed)
                delta = myPrice - peerPrice
            PeersNeeds.append(mostValueSticker)
        elif delta < 0:
            while delta < 0:
                mostValueSticker = needed.pop(-1)
                myPrice = calculatePrice(PeersNeeds)
                peerPrice = calculatePrice(needed)
                delta = myPrice - peerPrice
            needed.append(mostValueSticker)

        # Make deal and add the sticker to total stickers traded
        for sticker in needed:
            self.add_sticker(sticker)
            otherAgent.remove_repeated(sticker)
            self.count_sticker_traded()
        for sticker in PeersNeeds:
            otherAgent.add_sticker(sticker)
            self.remove_repeated(sticker)
            otherAgent.count_sticker_traded()

        # Check if album is already filled
        self.check_album_filled()
        otherAgent.check_album_filled()

    def check_album_filled(self):
        if len(self.obtained) == gameConfig.n:
            self.filled = True

    def next_intertial_frame(self):
        epsilon = 0.01
        sprite_width = gameConfig.sprite_width
        sprite_height = gameConfig.sprite_height
        if abs(self.x_speed) < 0+epsilon and abs(self.x_speed) < 0+epsilon:
            self.previous_inertial_frame[0] = 30
        elif abs(self.x_speed) > abs(self.y_speed):
            if self.x_speed < 0 and self.current_direction == "left":
                self.previous_inertial_frame[0] = (
                    self.previous_inertial_frame[0] + sprite_width) % (3*sprite_width)
            elif self.x_speed < 0 and self.current_direction != "left":
                self.previous_inertial_frame[0] = 0
                self.previous_inertial_frame[1] = sprite_height
                self.current_direction = "left"
            elif self.x_speed > 0 and self.current_direction == "right":
                self.previous_inertial_frame[0] = (
                    self.previous_inertial_frame[0] + sprite_width) % (3*sprite_width)
            elif self.x_speed > 0 and self.current_direction != "right":
                self.previous_inertial_frame[0] = 0
                self.previous_inertial_frame[1] = 2*sprite_height
                self.current_direction = "right"
        elif abs(self.y_speed) > abs(self.x_speed):
            if self.y_speed < 0 and self.current_direction == "up":
                self.previous_inertial_frame[0] = (
                    self.previous_inertial_frame[0] + sprite_width) % (3*sprite_width)
            elif self.y_speed < 0 and self.current_direction != "up":
                self.previous_inertial_frame[0] = 0
                self.previous_inertial_frame[1] = 3*sprite_height
                self.current_direction = "up"
            elif self.y_speed > 0 and self.current_direction == "down":
                self.previous_inertial_frame[0] = (
                    self.previous_inertial_frame[0] + 30) % 90
            elif self.y_speed > 0 and self.current_direction != "down":
                self.previous_inertial_frame[0] = 0
                self.previous_inertial_frame[1] = 0
                self.current_direction = "down"

        if self.state == "trading":
            self.previous_inertial_frame[0] = 30

        return self.previous_inertial_frame
