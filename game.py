import pygame
import os
import random
import schedule

class linedodger():
    class Player():
        def __init__(self, SCREEN, SCREEN_SIZE):
            self.size = 8
            self.SCREEN = SCREEN
            self.WIDTH = SCREEN_SIZE[0]
            self.HEIGHT = SCREEN_SIZE[1]
            self.x = self.WIDTH/2
            self.y = self.HEIGHT-20
            self.score = 0
            self.vel = round(SCREEN_SIZE[0]/228.5, 1)
            self.player = pygame.Rect(self.x, self.y, self.size, self.size)

        def update(self, lines):
            pressedkeys = pygame.key.get_pressed() #gets all pressed keys
            if pressedkeys[pygame.K_LEFT] and pressedkeys[pygame.K_RIGHT]:
                pass
            elif pressedkeys[pygame.K_LEFT]: #moves the player left if the left arrow is pressed
                self.x -= self.vel
            elif pressedkeys[pygame.K_RIGHT]: #moves the player right if the left arrow is pressed
                self.x += self.vel
            if self.x < self.size:
                self.x = self.size
            elif self.x > self.WIDTH - self.size:
                self.x = self.WIDTH - self.size
            pygame.draw.circle(self.SCREEN, (0, 255, 255), (self.x, self.y), self.size)
            self.player.topleft = self.x, self.y
            for line in lines:
                for chunck in line.chuncks: #checks for collisons
                    if self.player.colliderect(chunck):
                        print("Contact: Game Over")
                        self.score = 0
                        self.x = self.WIDTH/2
                        return -1
                    else:
                        line.chuncks.remove(chunck)

            return 0

    class Line():
        def __init__(self, SCREEN, SCREEN_SIZE):
            self.y = 0
            self.SCREEN = SCREEN
            self.WIDTH = SCREEN_SIZE[0]
            self.HEIGHT = SCREEN_SIZE[1]
            self.speed = 2
            self.width = 3
            self.block_size = round(SCREEN_SIZE[0]/20)
            self.num_of_chuncks = round(self.WIDTH/self.block_size)
            number_of_holes = random.randint(1, 3)
            self.holepositions = []
            self.chuncks = []
            for item in range(number_of_holes):
                chosen_one = random.randint(0, self.num_of_chuncks - 1)
                while True:
                    if chosen_one not in self.holepositions and (chosen_one - 1) not in self.holepositions and (chosen_one + 1) not in self.holepositions:
                        self.holepositions.append(chosen_one)
                        break

        def update(self):
            self.y += self.speed
            if self.y >= self.HEIGHT:
                return -1
            else:
                for number in range(self.num_of_chuncks):
                    if number in self.holepositions:
                        pass
                    else:
                        x = (number * self.block_size)
                        new_chunck = pygame.draw.rect(self.SCREEN, (255, 0, 0), (x, self.y, self.block_size, 3))
                        new_chunck.topleft = x, self.y
                        self.chuncks.append(new_chunck)
                return 0

    class Background:
        def __init__(self, WIDTH, HEIGHT):
            self.objects = []
            self.star = pygame.image.load(os.path.join("assets", "star.png")).convert_alpha()
            self.galaxy = pygame.image.load(os.path.join("assets", "galaxy.png")).convert_alpha()
            self.spawn_chance = 10
            self.max_objects = 100

        def sort_key(self, i):
            return i["size"]

        def update(self, SCREEN, WIDTH, HEIGHT, speed):
            SCREEN.fill((32, 25, 26))
            SCREEN.blit(self.galaxy, ((WIDTH-self.galaxy.get_width())/2, (HEIGHT-self.galaxy.get_height())/2))
            if len(self.objects) != self.max_objects:
                spawn = random.randint(0, self.spawn_chance)
                if spawn == self.spawn_chance:
                    new_object_size = random.randint(1, 10)
                    new_object_x = random.randint(0, WIDTH)
                    image = pygame.transform.scale(self.star, (new_object_size, new_object_size))
                    self.objects.append({"object": image, "size": new_object_size, "x": new_object_x, "y": -50})
            self.objects.sort(reverse=True, key=self.sort_key)
            for flying_object in self.objects:
                if flying_object["y"] > HEIGHT:
                    self.objects.remove(flying_object)
                else:
                    SCREEN.blit(flying_object["object"], (flying_object["x"], flying_object["y"]))
                    flying_object["y"] += (speed/30)*flying_object["size"]

    def updateWindow(self):
        self.SCREEN.fill((0, 0, 0))
        self.bg.update(self.SCREEN, self.WIDTH, self.HEIGHT, 10) #puts the BACKGROUND
        if self.started:
            update_player = self.player.update(self.lines)
            if update_player != 0:
                return update_player
            for line in self.lines:
                if line.update() == -1:
                    self.player.score += 1
                    self.lines.remove(line)
                    del line
            display_score = self.font.render(str(self.player.score), False, (255, 255, 255))
            self.SCREEN.blit(display_score, (self.WIDTH - 64*len(str(self.player.score)), 20))
        else:
            display_start = self.font.render("Press Space to Start", False, (255, 255, 255))
            self.SCREEN.blit(display_start, ((self.WIDTH - (30*len("Press Space to Start")))/2, (self.HEIGHT/2-32)))
        pygame.display.update() #updates/refreshes the SCREEN

    def new_line(self):
        new_line = self.Line(self.SCREEN, (self.WIDTH, self.HEIGHT))
        self.lines.append(new_line)

    def game_over(self, score): #:(
        for line in self.lines:
            self.lines.remove(line)
            del line

    def run(self):
        while self.started == False:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -2
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return -2
                    elif event.key == pygame.K_SPACE:
                        self.started = True
            self.updateWindow()
        create_new_lines = schedule.every(int(self.MIN)).seconds.to(int(self.MAX)).do(self.new_line)
        self.player.x = self.WIDTH/2
        while True:
            self.clock.tick(self.FPS) #makes sure that the game stays at 60 fps
            schedule.run_pending()
            if_error = self.updateWindow() #updates the window with the new player position
            if if_error == -1:
                return -1
            for event in pygame.event.get(): #checks if you close the window and then stops the game
                if event.type == pygame.QUIT:
                    return -2
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return -2
                    elif event.key == pygame.K_r:
                        return -1
        del self.player

    def main_loop(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Line Dodger")
        self.lines = []
        self.FPS = 60 #frames per second
        self.bg = self.Background(self.WIDTH, self.HEIGHT) #BACKGROUND
        self.MIN = 3 #min amount of time to spawn a line
        self.MAX = 5 #max amount of time to spawn a line
        self.clock = pygame.time.Clock()
        self.player = self.Player(self.SCREEN, (self.WIDTH, self.HEIGHT))
        pygame.init()
        pygame.font.init()
        pygame.mixer.init() #starts the player
        pygame.mixer.music.load(os.path.join("assets", "space_music.wav")) #loads the music file
        pygame.mixer.music.play(-1) #to play forever
        self.font = pygame.font.SysFont("Arial", 64)
        self.started = False
        while True:
            run_game = self.run()
            if run_game == -1:
                self.game_over(run_game)
            elif run_game == -2:
                break
            schedule.clear()
            self.player.score = 0

if __name__ == "__main__":
    WIDTH, HEIGHT = 640, 320 #size of the window
    game = linedodger()
    game.main_loop(WIDTH, HEIGHT)
