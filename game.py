import pygame, os, random, time, schedule, sys

from pygame.draw import line

WIDTH, HEIGHT = 1280, 720 #of the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Line Dodger")
retry = False

WHITE = (255, 255, 255)

lines = []
chuncks = []
min = 3.5
max = 5
linecount = 0

FPS = 60 #frames per second

background = pygame.image.load(os.path.join(os.getcwd(), "Line Dodger", "assets", "stars.jpg")) #background

def get_line_spaces():
    number_of_holes = random.randint(1, 3)
    holepositions = []
    for item in range(number_of_holes):
        chosen_one = random.randint(1, 40)
        while True:
            if chosen_one in holepositions:
                chosen_one = random.randint(1, 40)
            else:
                holepositions.append(chosen_one)
                break
    return holepositions

class Player():
    def __init__(self):
        self.size = 8
        self.x = 640
        self.vel = 3
        self.player = pygame.Rect(self.x, 576, self.size, self.size)
        pygame.draw.circle(screen, WHITE, (self.x, 640), self.size)
        print("[Player]: new player initialized")
    
    def update(self):
        for chunck in chuncks:
            if self.player.colliderect(chunck):
                print(chunck.y)
                print("Contact: Game Over")
                break
            else:
                chuncks.remove(chunck)
        pressedkeys = pygame.key.get_pressed() #gets all pressed keys
        if pressedkeys[pygame.K_LEFT]: #moves the player left if the left arrow is pressed
            self.x -= self.vel
        elif pressedkeys[pygame.K_RIGHT]: #moves the player right if the left arrow is pressed
            self.x += self.vel
        pygame.draw.circle(screen, WHITE, (self.x, 576), self.size)
        self.player.topleft = self.x, 576

class Line():
    def __init__(self):
        self.y = 0
        self.speed = 2
        self.holepositions = get_line_spaces()
        for number in range(1, 40):
            if number in self.holepositions:
                pass
            else:
                x = number * 32
                pygame.draw.rect(screen, WHITE, (x, self.y, 32, 3))
        print(f"[Line]: new line initialized")

    def update(self):
        self.y += self.speed
        if self.y >= 720:
            print(f"[Line]: removed")
            del lines[linecount]
        else:
            for number in range(1, 41):
                if number in self.holepositions:
                    pass
                else:
                    x = (number * 32) - 32
                    new_chunck = pygame.draw.rect(screen, WHITE, (x, self.y, 32, 3))
                    new_chunck.topleft = x, self.y
                    chuncks.append(new_chunck)

def updateWindow(player, lines):
    screen.fill(WHITE)
    screen.blit(background, (0, 0)) #puts the background
    player.update()
    for line in lines:
        line.update()
    pygame.display.update() #updates/refreshes the screen

def playmusic():
    pygame.mixer.init() #starts the player
    pygame.mixer.music.load(os.path.join(os.getcwd(), "Line Dodger", "assets", "space_music.wav")) #loads the music file
    pygame.mixer.music.play(-1) #to play forever
    print("[Music]: Started")

def new_line():
    new_line = Line()
    lines.append(new_line)
    print(lines)

def main():
    run = True
    clock = pygame.time.Clock()
    pygame.init()
    print("[Pygame]: initialized")
    playmusic()
    player = Player()
    schedule.every(int(min)).seconds.to(int(max)).do(new_line)
    new_line()
    while run:
        clock.tick(FPS) #makes sure that the game stays at 60 fps
        for event in pygame.event.get(): #checks if you close the window and then stops the game
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                print("[Music]: Stopped")
                pygame.quit() #closes the tab
                print("Game Closed")
                run = False
                sys.exit()
        schedule.run_pending()
        updateWindow(player, lines) #updates the window with the new player position

main()