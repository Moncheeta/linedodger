import pygame, os, random, schedule

WIDTH, HEIGHT = 1280, 720 #of the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Line Dodger")
retry = False

#Colors
WHITE = (255, 255, 255)

lines = []
chuncks = []
min = 3.5
max = 5
linecount = 0

FPS = 60 #frames per second

background = pygame.image.load(os.path.join("assets", "stars.jpg")) #background

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
        self.x = 632
        self.y = 712
        self.vel = 3
        self.score = 0
        self.player = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.size)
        print("[Player]: new player initialized")

    def update(self):
        if self.x > 1280:
            self.x -= 1
        elif self.x < 0:
            self.x += 1
        for chunck in chuncks:
            if self.player.colliderect(chunck):
                print("Contact: Game Over")
                game_over(self.score)
                chuncks.remove(chunck)
                break
            else:
                chuncks.remove(chunck)
        pressedkeys = pygame.key.get_pressed() #gets all pressed keys
        if self.x >= 1280 - self.size:
            self.x -= 1
        elif self.x <= 0 + self.size:
            self.x += 1
        else:
            if pressedkeys[pygame.K_LEFT]: #moves the player left if the left arrow is pressed
                self.x -= self.vel
            elif pressedkeys[pygame.K_RIGHT]: #moves the player right if the left arrow is pressed
                self.x += self.vel
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.size)
        self.player.topleft = self.x, self.y

class Line():
    def __init__(self):
        self.y = 0
        self.speed = 2
        self.width = 3
        self.holepositions = get_line_spaces()
        for number in range(1, 40):
            if number in self.holepositions:
                pass
            else:
                x = number * 32
                pygame.draw.rect(screen, WHITE, (x, self.y, 32, self.width))
        print(f"[Line]: new line initialized")

    def update(self):
        self.y += self.speed
        if self.y >= 720:
            print(f"[Line]: removed")
            del lines[linecount]
            return "addScore"
        else:
            for number in range(1, 41):
                if number in self.holepositions:
                    pass
                else:
                    x = (number * 32) - 32
                    new_chunck = pygame.draw.rect(screen, WHITE, (x, self.y, 32, 3))
                    new_chunck.topleft = x, self.y
                    chuncks.append(new_chunck)

def updateWindow(player, lines, font):
    screen.fill(WHITE)
    screen.blit(background, (0, 0)) #puts the background
    player.update()
    for line in lines:
        check = line.update()
        if check == "addScore":
            player.score += 1
    display_score = font.render(str(player.score), False, (WHITE))
    screen.blit(display_score, (1248 - 16*len(str(player.score)), 20))
    pygame.display.update() #updates/refreshes the screen

def playmusic():
    pygame.mixer.init() #starts the player
    pygame.mixer.music.load(os.path.join("assets", "space_music.wav")) #loads the music file
    pygame.mixer.music.play(-1) #to play forever
    print("[Music]: Started")

def new_line():
    new_line = Line()
    lines.append(new_line)
    print(lines)

def game_over(score): #:(
    print(score)

def run():
    run = True
    clock = pygame.time.Clock()
    pygame.init()
    print("[Pygame]: initialized")
    pygame.font.init()
    font = pygame.font.SysFont("arial", 64)
    playmusic()
    player = Player()
    schedule.every(int(min)).seconds.to(int(max)).do(new_line)
    new_line()
    while run:
        clock.tick(FPS) #makes sure that the game stays at 60 fps
        schedule.run_pending()
        updateWindow(player, lines, font) #updates the window with the new player position
        for event in pygame.event.get(): #checks if you close the window and then stops the game
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                print("[Music]: Stopped")
                pygame.quit() #closes the tab
                print("Game Closed")
                run = False

run()