import pygame
import os
import sys
import random
import schedule
import itertools

WIDTH, HEIGHT = 640, 320 #size of the window
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Line Dodger")
retry = False

#Colors
WHITE = (255, 255, 255)

lines = []
MIN = 3 #min amount of time to spawn a line
MAX = 5 #max amount of time to spawn a line
FPS = 60 #frames per second

BACKGROUND = pygame.image.load(os.path.join("assets", "stars.jpg")).convert() #BACKGROUND

"""
Todo:
"""

class Player():
    def __init__(self):
        self.size = 8
        self.x = WIDTH/2
        self.y = HEIGHT-20
        self.score = 0
        self.vel = 2.5
        self.player = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.circle(SCREEN, WHITE, (self.x, self.y), self.size)

    def update(self):
        pressedkeys = pygame.key.get_pressed() #gets all pressed keys
        if pressedkeys[pygame.K_LEFT]: #moves the player left if the left arrow is pressed
            self.x -= self.vel
        elif pressedkeys[pygame.K_RIGHT]: #moves the player right if the left arrow is pressed
            self.x += self.vel
        if self.x < self.size:
            self.x = self.size
        elif self.x > WIDTH - self.size:
            self.x = WIDTH - self.size
        pygame.draw.circle(SCREEN, WHITE, (self.x, self.y), self.size)
        self.player.topleft = self.x, self.y
        for line in lines:
            for chunck in line.chuncks: #checks for collisons
                if self.player.colliderect(chunck):
                    print("Contact: Game Over")
                    self.score = 0
                    self.x = WIDTH/2
                    return -1
                else:
                    line.chuncks.remove(chunck)

        return 0

class Line():
    def __init__(self):
        self.y = 0
        self.speed = 2
        self.width = 3
        self.block_size = 32
        self.num_of_chuncks = round(WIDTH/self.block_size)
        number_of_holes = random.randint(1, 3)
        self.holepositions = []
        self.chuncks = []
        for item in range(number_of_holes):
            chosen_one = random.randint(0, self.num_of_chuncks - 1)
            while True:
                if not chosen_one in self.holepositions:
                    self.holepositions.append(chosen_one)
                    break

    def update(self):
        self.y += self.speed
        if self.y >= HEIGHT:
            return -1
        else:
            for number in range(self.num_of_chuncks):
                if number in self.holepositions:
                    pass
                else:
                    x = (number * self.block_size)
                    new_chunck = pygame.draw.rect(SCREEN, WHITE, (x, self.y, self.block_size, 3))
                    new_chunck.topleft = x, self.y
                    self.chuncks.append(new_chunck)
            return 0

def updateWindow(player, lines, font):
    SCREEN.fill(WHITE)
    SCREEN.blit(BACKGROUND, (0, 0)) #puts the BACKGROUND
    update_player = player.update()
    if update_player != 0:
        return update_player
    for line in lines:
        if line.update() == -1:
            player.score += 1
            lines.remove(line)
            del line
    display_score = font.render(str(player.score), False, (WHITE))
    SCREEN.blit(display_score, (WIDTH - 64*len(str(player.score)), 20))
    pygame.display.update() #updates/refreshes the SCREEN

def playmusic():
    pygame.mixer.init() #starts the player
    pygame.mixer.music.load(os.path.join("assets", "space_music.wav")) #loads the music file
    pygame.mixer.music.play(-1) #to play forever

def new_line():
    new_line = Line()
    lines.append(new_line)

def game_over(score): #:(
    for line in lines: 
        lines.remove(line)
        del line

clock = pygame.time.Clock()
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial", 64)
playmusic()
player = Player()

def run():
    create_new_lines = schedule.every(int(MIN)).seconds.to(int(MAX)).do(new_line)
    player.x = WIDTH/2
    while True:
        clock.tick(FPS) #makes sure that the game stays at 60 fps
        schedule.run_pending()
        if_error = updateWindow(player, lines, font) #updates the window with the new player position
        if if_error == -1:
            return player.score
        for event in pygame.event.get(): #checks if you close the window and then stops the game
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_r:
                    return -1

while True:
    run_game = run()
    if run_game != -1:
        game_over(run_game)
    schedule.clear()
    player.score = 0
