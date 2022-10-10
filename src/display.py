import pygame
import random
import time
from game_config import gameConfig, WHITE, FONT, FPS, WIDTH, HEIGHT, WIN
from agent import Agent

L = [None]*4
endStates = []


def draw_window(agents):
    WIN.fill(WHITE)
    WIN.blit(gameConfig.day_count_text, gameConfig.day_count_text_container)
    for agent in agents:
        WIN.blit(agent.aficionado_image, (agent.x, agent.y),
                 tuple(agent.next_intertial_frame()))
    pygame.display.update()


def update_trades(agent, frame_time):
    # finish trades
    if agent.state == "trading":
        agent.frames_to_finish_trade -= frame_time
        if agent.frames_to_finish_trade <= 0:
            agent.state = "idle"
            agent.frames_to_finish_trade = 0


def check_collision_for_trading(agents):
    rectangles = []
    collisions = set()
    for agent in agents:
        rectangles.append(agent.get_rectangle())

    for index in range(len(agents)):

        if already_collided(index, agents[index], collisions):
            continue

        possible_collisions_indexes = rectangles[index].collidelistall(
            rectangles)
        while index in possible_collisions_indexes:
            possible_collisions_indexes.remove(index)
        while agents[index].last_traded_with in possible_collisions_indexes:
            possible_collisions_indexes.remove(agents[index].last_traded_with)

        if len(possible_collisions_indexes) > 0:
            for possible_collision_index in possible_collisions_indexes:
                if already_collided(possible_collision_index, agents[possible_collision_index], collisions):
                    continue
                else:
                    collisions.add((index, possible_collision_index))
                    break
    sprite_width = gameConfig.sprite_width
    speed_limit = gameConfig.speed_limit
    for collision in collisions:
        agents[collision[0]].state = "trading"
        agents[collision[1]].state = "trading"
        agents[collision[0]].frames_to_finish_trade = 60
        agents[collision[1]].frames_to_finish_trade = 60
        agents[collision[0]].last_traded_with = collision[1]
        agents[collision[1]].last_traded_with = collision[0]

        agents[collision[1]].x = agents[collision[0]].x + sprite_width
        agents[collision[1]].y += - \
            (agents[collision[1]].y - agents[collision[0]].y)/2
        agents[collision[1]].x_speed = -speed_limit
        agents[collision[0]].x_speed = speed_limit
        agents[collision[1]].y_speed = 0
        agents[collision[0]].y_speed = 0

        agents[collision[0]].trade(agents[collision[1]])


def buy_envelopes(agents, quantity):
    for agent in agents:
        for i in range(0, quantity):
            agent.open_envelope()


def already_collided(index, agent, collisions):

    # If this agent is during this frame is still trading, he already collided with someone else
    if agent.state == "trading":
        return True

    # already in recent collisions
    for collision in collisions:
        if index in collision:
            return True

    return False


def generateReport(agents):
    agents_filled = []
    for agent in agents:
        if agent.is_filled():
            agents_filled.append(agent)

    if len(agents_filled) == 0:
        print("No albums were filled in this simulation")
    for agent in agents_filled:
        print("Generating report for agent--- \nOpened envelopes:" +
              str(agent.envelopesOpened) + "\nStickers traded: " + str(agent.stickersTraded))
    print("Agents with album filled " + str(len(agents_filled)))
    if len(agents_filled) > 0:
        print("Average envelopes opened " +
              str(sum([agent.get_envelopes_opened() for agent in agents_filled])/len(agents_filled)))


def event_1(agents, quantity):  # Compra inicial
    L[0] = float('inf')
    buy_envelopes(agents, quantity)


def event_2(agents, quantity):  # Nuevo dia
    gameConfig.days_elapsed += 1
    gameConfig.day_count_text = FONT.render("Day: " + str(gameConfig.days_elapsed),
                                 True, (0, 255, 0), (0, 0, 255))
    gameConfig.day_count_text_container = gameConfig.day_count_text.get_rect()
    time.sleep(0.2)
    if gameConfig.days_elapsed == gameConfig.number_of_days:
        L[1] = float('inf')
    else:
        L[1] += 2
    buy_envelopes(agents, quantity)


def event_3(agents, clock, FPS, day_duration):  # Salir a tradear
    if gameConfig.days_elapsed == gameConfig.number_of_days:
        L[2] = float('inf')
    else:
        L[2] += 2
    run = True
    steps = 0
    while run:
        if steps >= day_duration:
            break
        steps += 1
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                L[1] = float('inf')
                L[2] = float('inf')
        for agent in agents:
            agent.next_random_move()
            update_trades(agent, 1)

        check_collision_for_trading(agents)

        draw_window(agents)


def event_4():  # Fin del mundo
    pygame.quit()


def initialize():  # Initial parameters
    global endStates, WIDTH, HEIGHT, WIN
    gameConfig.days_elapsed = 0
    # Create window
    WIDTH, HEIGHT = 1500, 800
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("FIFAlbum simulation")
    gameConfig.day_count_text_container.center = (WIDTH//2, HEIGHT//10)
    # Set up initial events
    L[0] = 0
    L[1] = 1
    L[2] = 2
    L[3] = 1 + 2 * gameConfig.number_of_days
    # Set up end states
    endStates = [4]
    # Initial parameters
    agents = [Agent(random.uniform(0, WIDTH), random.uniform(
        0, HEIGHT), x % 4) for x in range(gameConfig.number_of_agents)]
    clock = pygame.time.Clock()
    return agents, clock


def manageTimeAndSpace():
    nextEvent = -1
    nextEventTime = float('inf')
    print("LEN", len(L))
    for i in range(len(L)):
        print("\t try", i, "->", L[i])
        if L[i] < nextEventTime:
            nextEvent = i+1
            nextEventTime = L[i]
    return nextEvent


def main():
    agents, clock = initialize()
    End = False
    Error = False
    while (not End and not Error):
        i = manageTimeAndSpace()
        print("Event ", i)
        if i == 1:
            event_1(agents, gameConfig.initial_purchase)
        if i == 2:
            event_2(agents, gameConfig.daily_purchase)
        if i == 3:
            event_3(agents, clock, FPS, gameConfig.day_duration)
        if i == 4:
            event_4()
        if i == -1:
            Error = True
        if i in endStates:
            End = True
    generateReport(agents)


if __name__ == "__main__":
    main()
