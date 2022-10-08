import pygame
import os
import random


#window
WIDTH,HEIGHT = 1600,1000
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("FIFAlbum simulation")

#useful constants
WHITE = (255,255,255)
number_of_agents = 150
FPS=15
speed_limit = 4
sprite_width=30
sprite_height=32
AFICIONADO1 = pygame.image.load(os.path.join("Assets","CharactersSprites1.png"))
AFICIONADO2 = pygame.image.load(os.path.join("Assets","CharactersSprites2.png"))
AFICIONADO3 = pygame.image.load(os.path.join("Assets","CharactersSprites3.png"))

def draw_window(agents):
    WIN.fill(WHITE)
    for agent in agents:
        WIN.blit(agent.aficionado_image,(agent.x,agent.y),tuple(agent.next_intertial_frame()))
    pygame.display.update()

def update_trades(agent,frame_time):
    #finish trades
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

        if already_collided(index,agents[index],collisions):
            continue

        possible_collisions_indexes = rectangles[index].collidelistall(rectangles)
        while index in possible_collisions_indexes: possible_collisions_indexes.remove(index)
        while agents[index].last_traded_with in possible_collisions_indexes: possible_collisions_indexes.remove(agents[index].last_traded_with)

        if len(possible_collisions_indexes) > 0:
            for possible_collision_index in possible_collisions_indexes:
                if already_collided(possible_collision_index,agents[possible_collision_index],collisions):
                    continue
                else:
                    collisions.add((index,possible_collision_index))
                    break
    
    for collision in collisions:
        agents[collision[0]].state = "trading"
        agents[collision[1]].state = "trading"
        agents[collision[0]].frames_to_finish_trade = 60
        agents[collision[1]].frames_to_finish_trade = 60
        agents[collision[0]].last_traded_with = collision[1]
        agents[collision[1]].last_traded_with = collision[0]

        agents[collision[1]].x = agents[collision[0]].x + sprite_width
        agents[collision[1]].y += -(agents[collision[1]].y - agents[collision[0]].y)/2 
        agents[collision[1]].x_speed = -speed_limit
        agents[collision[0]].x_speed = speed_limit
        agents[collision[1]].y_speed = 0
        agents[collision[0]].y_speed = 0





def already_collided(index,agent,collisions):

    #If this agent is during this frame is still trading, he already collided with someone else
    if agent.state == "trading":
        return True
    

    #already in recent collisions
    for collision in collisions:
        if index in collision:
            return True
    
    

    return False




    

def main():
    agents = [Agent(random.uniform(0, WIDTH),random.uniform(0, HEIGHT),x%4) for x in range(number_of_agents)]
    clock = pygame.time.Clock()
    run = True
    while run:
        frame_time = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for agent in agents:
            agent.next_random_move()
            update_trades(agent,1)
        
        check_collision_for_trading(agents)
        draw_window(agents)
    pygame.quit()



class Agent:
    def __init__(self,initialX,initialY,aficionado_number):
        self.x = initialX
        self.y = initialY
        self.x_speed = 0
        self.y_speed = 0
        self.previous_inertial_frame = [0,0,30,32]
        self.current_direction = "down"
        self.aficionado_image = AFICIONADO1
        if aficionado_number == 0:
            self.aficionado_image = AFICIONADO1
        elif aficionado_number == 1:
            self.aficionado_image = AFICIONADO2
        elif aficionado_number == 2:
            self.aficionado_image = AFICIONADO3
        self.state = "idle" #idle,trading
        self.frames_to_finish_trade = 0
        self.last_traded_with = -1
    
    def get_rectangle(self):
        return pygame.Rect(self.x,self.y,sprite_width,sprite_height)
    
    def next_random_move(self):

        if self.state == "trading":
            return

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


        

    def next_intertial_frame(self):
        epsilon = 0.01
        if abs(self.x_speed) < 0+epsilon and abs(self.x_speed) < 0+epsilon:
            self.previous_inertial_frame[0] = 30
        elif abs(self.x_speed) > abs(self.y_speed):
            if self.x_speed < 0 and self.current_direction == "left":
                self.previous_inertial_frame[0] = (self.previous_inertial_frame[0] + sprite_width)%(3*sprite_width)
            elif self.x_speed < 0 and self.current_direction != "left":
                self.previous_inertial_frame[0] = 0
                self.previous_inertial_frame[1] = sprite_height
                self.current_direction = "left"
            elif self.x_speed > 0 and self.current_direction == "right":
                self.previous_inertial_frame[0] = (self.previous_inertial_frame[0] + sprite_width)%(3*sprite_width)
            elif self.x_speed > 0 and self.current_direction != "right":
                self.previous_inertial_frame[0] = 0
                self.previous_inertial_frame[1] = 2*sprite_height
                self.current_direction = "right"
        elif abs(self.y_speed) > abs(self.x_speed):
            if self.y_speed < 0 and self.current_direction == "up":
                self.previous_inertial_frame[0] = (self.previous_inertial_frame[0] + sprite_width)%(3*sprite_width)
            elif self.y_speed < 0 and self.current_direction != "up":
                self.previous_inertial_frame[0] = 0
                self.previous_inertial_frame[1] = 3*sprite_height
                self.current_direction = "up"
            elif self.y_speed > 0 and self.current_direction == "down":
                self.previous_inertial_frame[0] = (self.previous_inertial_frame[0] + 30)%90
            elif self.y_speed > 0 and self.current_direction != "down":
                self.previous_inertial_frame[0] = 0
                self.previous_inertial_frame[1] = 0
                self.current_direction = "down"

        if self.state == "trading":
            self.previous_inertial_frame[0] = 30
        
        return self.previous_inertial_frame



if __name__ == "__main__":
    main()
