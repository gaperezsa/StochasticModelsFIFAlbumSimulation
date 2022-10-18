import pygame
import random
import time
from agent import Agent, AgentStates
from global_context import context

pygame.init()
font = pygame.font.Font("freesansbold.ttf", 32)
day_count_label = font.render("Day: 0", True, (50, 50, 50), (255, 255, 255))
day_count_label_rect = day_count_label.get_rect()

# useful constants
WHITE = (255, 255, 255)


class Simulator:
    def __init__(self, config):
        self.config = config

    L = [None]*4
    end_states = []

    def draw_window(self, agents):
        global day_count_label, day_count_label_rect
        context.win.fill(WHITE)
        context.win.blit(day_count_label, day_count_label_rect)
        for agent in agents:
            context.win.blit(agent.character, (agent.x, agent.y),
                             tuple(agent.next_intertial_frame()))
        pygame.display.update()

    def update_trades(self, agent, frame_time):
        # finish trades
        if agent.state == AgentStates.TRADING:
            agent.frames_to_finish_trade -= frame_time
            if agent.frames_to_finish_trade <= 0:
                agent.state = AgentStates.IDLE
                agent.frames_to_finish_trade = 0

    def check_collision_for_trading(self, agents):
        config = self.config
        rectangles = []
        collisions = set()
        for agent in agents:
            rectangles.append(agent.get_rectangle())

        for index in range(len(agents)):

            if self.already_collided(index, agents[index], collisions):
                continue

            possible_collisions_indexes = rectangles[index].collidelistall(
                rectangles)
            while index in possible_collisions_indexes:
                possible_collisions_indexes.remove(index)
            while agents[index].last_traded_with in possible_collisions_indexes:
                possible_collisions_indexes.remove(
                    agents[index].last_traded_with)

            if len(possible_collisions_indexes) > 0:
                for possible_collision_index in possible_collisions_indexes:
                    if self.already_collided(possible_collision_index, agents[possible_collision_index], collisions):
                        continue
                    else:
                        collisions.add((index, possible_collision_index))
                        break

        for collision in collisions:
            agents[collision[0]].state = AgentStates.TRADING
            agents[collision[1]].state = AgentStates.TRADING
            agents[collision[0]].frames_to_finish_trade = 60
            agents[collision[1]].frames_to_finish_trade = 60
            agents[collision[0]].last_traded_with = collision[1]
            agents[collision[1]].last_traded_with = collision[0]

            agents[collision[1]].x = agents[collision[0]].x + \
                config.sprite_width
            agents[collision[1]].y += - \
                (agents[collision[1]].y - agents[collision[0]].y)/2
            agents[collision[1]].x_speed = -config.speed_limit
            agents[collision[0]].x_speed = config.speed_limit
            agents[collision[1]].y_speed = 0
            agents[collision[0]].y_speed = 0

            agents[collision[0]].trade(agents[collision[1]])

    def buy_envelopes(self, agents, quantity):
        for agent in agents:
            for i in range(0, quantity):
                agent.open_envelope()

    def already_collided(self, index, agent, collisions):

        # If this agent is during this frame is still trading, he already collided with someone else
        if agent.state == AgentStates.TRADING:
            return True

        # already in recent collisions
        for collision in collisions:
            if index in collision:
                return True

        return False

    def print_report(self, agents):
        agents_filled = []
        for agent in agents:
            if agent.is_filled():
                agents_filled.append(agent)

        if len(agents_filled) == 0:
            print("No albums were filled in this simulation")
        for agent in agents_filled:
            print("Generating report for agent--- \nOpened envelopes:" +
                  str(agent.envelopes_opened) + "\nStickers traded: " + str(agent.stickers_traded))
        print("Agents with album filled " + str(len(agents_filled)))
        if len(agents_filled) > 0:
            print("Average envelopes opened " +
                  str(sum([agent.get_envelopes_opened() for agent in agents_filled])/len(agents_filled)))

    def initial_purchase(self, agents, quantity):  # Compra inicial
        self.L[0] = float('inf')
        self.buy_envelopes(agents, quantity)

    def new_day(self, agents, quantity):  # Nuevo dia
        config = self.config
        global day_count_label, day_count_label_rect
        config.days_elapsed += 1
        day_count_label = font.render("Day: " + str(config.days_elapsed),
                                      True, (50, 50, 50), (255, 255, 255))
        day_count_label_rect = day_count_label.get_rect()
        time.sleep(0.2)
        if config.days_elapsed == config.number_of_days:
            self.L[1] = float('inf')
        else:
            self.L[1] += 2
        self.buy_envelopes(agents, quantity)

    def trade(self, agents, clock):  # Salir a tradear
        config = self.config
        if config.days_elapsed == config.number_of_days:
            self.L[2] = float('inf')
        else:
            self.L[2] += 2
        run = True
        steps = 0
        while run:
            if steps >= config.day_duration:
                break
            steps += 1
            clock.tick(config.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.L[1] = float('inf')
                    self.L[2] = float('inf')
            for agent in agents:
                agent.next_random_move()
                self.update_trades(agent, 1)

            self.check_collision_for_trading(agents)

            self.draw_window(agents)

    def finish(self):  # Fin del mundo
        pygame.quit()

    def initialize(self):  # Initial parameters
        config = self.config
        global day_count_label_rect
        config.days_elapsed = 0
        # Create window
        context.width, context.height = 1500, 800
        context.win = pygame.display.set_mode((context.width, context.height))
        pygame.display.set_caption("FIFAlbum simulation")
        day_count_label_rect.center = (context.width//2, context.height//10)
        # Set up initial events
        self.L[0] = 0
        self.L[1] = 1
        self.L[2] = 2
        self.L[3] = 1 + 2 * config.number_of_days
        # Set up end states
        self.end_states = [4]
        # Initial parameters
        agents = [Agent(random.uniform(0, context.width), random.uniform(
            0, context.height), x % 4, self.config) for x in range(config.number_of_agents)]
        clock = pygame.time.Clock()
        return agents, clock

    def get_next_event(self):
        nextEvent = -1
        nextEventTime = float('inf')
        print("LEN", len(self.L))
        for i in range(len(self.L)):
            print("\t try", i, "->", self.L[i])
            if self.L[i] < nextEventTime:
                nextEvent = i+1
                nextEventTime = self.L[i]
        return nextEvent

    def simulate(self):
        config = self.config
        agents, clock = self.initialize()
        end = False
        error = False
        while (not end and not error):
            i = self.get_next_event()
            print("Event ", i)
            if i == 1:
                self.initial_purchase(agents, config.initial_purchase)
            if i == 2:
                self.new_day(agents, config.daily_purchase)
            if i == 3:
                self.trade(agents, clock)
            if i == 4:
                self.finish()
            if i == -1:
                error = True
            if i in self.end_states:
                end = True
        self.print_report(agents)
