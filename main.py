import pygame
import os
import random


#window
WIDTH,HEIGHT = 1600,1000
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("FIFAlbum simulation")

#useful constants
WHITE = (255,255,255)
number_of_agents = 4
FPS=10
speed_limit = 2
AFICIONADO1 = pygame.image.load(os.path.join("Assets","CharactersSprites1.png"))
AFICIONADO2 = pygame.image.load(os.path.join("Assets","CharactersSprites2.png"))
AFICIONADO3 = pygame.image.load(os.path.join("Assets","CharactersSprites3.png"))

def draw_window(agents):
    WIN.fill(WHITE)
    for agent in agents:
        WIN.blit(agent.aficionado_image,(agent.x,agent.y),tuple(agent.next_intertial_frame()))
    pygame.display.update()

def main():
    agents = [Agent(200*x+100,200*x+100,x%4) for x in range(number_of_agents)]
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for agent in agents:
            agent.next_move()
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
    
    def next_move(self):
        self.x_speed += random.uniform(-1, 1)
        self.y_speed += random.uniform(-1, 1)
        self.x_speed = speed_limit if self.x_speed > speed_limit else self.x_speed
        self.x_speed = -speed_limit if self.x_speed < -speed_limit else self.x_speed
        self.y_speed = speed_limit if self.y_speed > speed_limit else self.y_speed
        self.y_speed = -speed_limit if self.y_speed < -speed_limit else self.y_speed

        self.x += self.x_speed
        self.y += self.y_speed

    def next_intertial_frame(self):
        epsilon = 0.01
        if abs(self.x_speed) < 0+epsilon and abs(self.x_speed) < 0+epsilon:
            self.previous_inertial_frame[0] = 30
        elif abs(self.x_speed) > abs(self.y_speed):
            if self.x_speed < 0 and self.current_direction == "left":
                self.previous_inertial_frame[0] = (self.previous_inertial_frame[0] + 30)%90
                return self.previous_inertial_frame
            elif self.x_speed < 0 and self.current_direction != "left":
                self.previous_inertial_frame[0] = 0
                self.previous_inertial_frame[1] = 32
                self.current_direction = "left"
            elif self.x_speed > 0 and self.current_direction == "right":
                self.previous_inertial_frame[0] = (self.previous_inertial_frame[0] + 30)%90
                return self.previous_inertial_frame
            elif self.x_speed > 0 and self.current_direction != "right":
                self.previous_inertial_frame[0] = 0
                self.previous_inertial_frame[1] = 64
                self.current_direction = "right"
        elif abs(self.y_speed) > abs(self.x_speed):
            if self.y_speed < 0 and self.current_direction == "down":
                self.previous_inertial_frame[0] = (self.previous_inertial_frame[0] + 30)%90
                return self.previous_inertial_frame
            elif self.y_speed < 0 and self.current_direction != "down":
                self.previous_inertial_frame[0] = 0
                self.previous_inertial_frame[1] = 96
                self.current_direction = "down"
            elif self.y_speed > 0 and self.current_direction == "up":
                self.previous_inertial_frame[0] = (self.previous_inertial_frame[0] + 30)%90
                return self.previous_inertial_frame
            elif self.y_speed > 0 and self.current_direction != "up":
                self.previous_inertial_frame[0] = 0
                self.previous_inertial_frame[1] = 0
                self.current_direction = "up"
        
        return self.previous_inertial_frame



if __name__ == "__main__":
    main()
