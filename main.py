"""
Dzięgielewska Marta
Flappy Bee
14.01.2020
"""

import pygame
import random
import os
import time
import sys
import pygame.surface

pygame.init()
pygame.font.init()
pygame.mixer.init()

clock = pygame.time.Clock()

# size of the app window
WIDTH = 500
HEIGHT = 600

LightGreen = (107, 255, 91)
Blue = (172, 192, 236)
Green = (120, 255, 57)
DarkGreen = (62, 99, 22)
DarkBlue = (5, 10, 21)

pygame.display.set_caption("FlappyBee")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# adjusting pictures
BEE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "pszczola.png")).convert_alpha(), (500, 500))
BG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "tło.png")).convert_alpha(), (500, 600))
GROUND = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "ground.png")).convert_alpha(), (500, 150))
TRUNK = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "trunk.png")).convert_alpha(), (250, 500))
HONEY = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "honey.png")).convert_alpha(), (70, 70))
END1 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "endbee1.png")).convert_alpha(), (100, 100))
END2 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "endbee2.png")).convert_alpha(), (220, 220))

SCOREFONT = pygame.font.SysFont("Comic Sans", 30)
BONUSFONT = pygame.font.SysFont("Comic Sans", 30)
ENDFONT = pygame.font.SysFont("Times New Roman", 40)

# adding sounds to the game
BUZZ = pygame.mixer.Sound('sounds/beebonus.wav')
BUZZ.set_volume(0.2)
FOREST = pygame.mixer.Sound('sounds/forest.wav')
FOREST.set_volume(0.2)
PUNCH = pygame.mixer.Sound('sounds/punch.wav')
PUNCH.set_volume(0.2)


# placing texts on the screen
def title(txt, x, y, size):
    cz = pygame.font.SysFont("Times New Roman", size)
    rend = cz.render(txt, True, LightGreen)
    x = (WIDTH - rend.get_rect().width) / 2
    y = (HEIGHT - rend.get_rect().height) / 4 * 3
    screen.blit(rend, (x, y))

    pygame.display.update()


def menu(txt, x, y, size):
    cz = pygame.font.SysFont("Times New Roman", size)
    rend = cz.render(txt, True, Blue)
    x = (WIDTH - rend.get_rect().width) / 2
    y = (HEIGHT - rend.get_rect().height) / 4 * 3
    screen.blit(rend, (x, y - 50))

    pygame.display.update()


def menu1(txt, x, y, size):
    cz = pygame.font.SysFont("Times New Roman", size)
    rend = cz.render(txt, True, Blue)
    # centering the text
    x = (WIDTH - rend.get_rect().width) / 2
    y = (HEIGHT - rend.get_rect().height) / 2
    screen.blit(rend, (x, y - 75))

    pygame.display.update()


def logo():
    logo_img = pygame.image.load(os.path.join('imgs', 'logo.png'))
    screen.blit(logo_img, (-25, 100))

    pygame.display.update()


def lose(txt, text, x, y, size, score):
    cz = pygame.font.SysFont("Times New Roman", size)
    rend = cz.render(txt, True, Blue)
    text = ENDFONT.render("your score: " + str(score), True, Blue)
    screen.blit(text, (135, 280))
    x = (WIDTH - rend.get_rect().width) / 2
    y = (HEIGHT - rend.get_rect().height) / 2 - 100
    screen.blit(rend, (x, y))

    pygame.display.update()


def end():
    txt = pygame.font.SysFont("Times New Roman", 17)
    text = txt.render("If you want to play again, click 1, if you want to exit, click 3", True, Blue)
    screen.blit(text, (40, 450))

    pygame.display.update()


class Bee:
    ANIMATION_TIME = 5
    MAX_ROTATION = 30
    ROT_VEL = 20
    BEE = BEE_IMG

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.BEE
        # drawing hitbox over the element
        self.hitbox = (self.x + 220, self.y + 225, 50, 50)

    def jump(self):
        self.vel = -9.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # how many pixels we are going up or down
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:
            d = 16
        if d < 0:
            d -= 2

        self.y = self.y + d

        # bee can rotate while falling down
        if d < 0 or self.y < self.height:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, screen):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.BEE
            self.img_count = 0

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        screen.blit(rotated_image, new_rect.topleft)
        self.hitbox = (self.x + 220, self.y + 225, 50, 50)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def hit(self, score):
        screen.fill(DarkBlue)
        screen.blit(END1, (100, 100))
        screen.blit(END2, (240, 275))
        lose("YOU LOST", "your points: " + str(score), 40, 100, 70, score)
        end()
        time.sleep(2)

        # chance of playing again
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        FOREST.play(-1)
                        main()
                    if event.key == pygame.K_3:
                        sys.exit()


class Ground:
    VEL = 7.5
    WIDTH = GROUND.get_width()
    IMG = GROUND

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        # drawing hitbox over the element
        self.hitbox1 = (self.x1, self.y + 100, 500, 50)
        self.hitbox2 = (self.x2, self.y + 100, 500, 50)

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # appearing alternately
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, screen):
        screen.blit(self.IMG, (self.x1, self.y))
        screen.blit(self.IMG, (self.x2, self.y))
        self.hitbox1 = (self.x1, self.y + 100, 500, 50)
        self.hitbox2 = (self.x2, self.y + 100, 500, 50)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox1, 2)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox2, 2)


class Trunk:
    GAP = 200
    VEL = 7.5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.TOPTRUNK = pygame.transform.flip(TRUNK, False, True)
        self.BOTTOMTRUNK = TRUNK
        self.passed = False
        self.set_height()
        self.hitboxtop = (self.x + 80, self.top, 80, 490)
        self.hitboxbottom = (self.x + 80, self.bottom + 10, 80, 490)

    def set_height(self):
        # every trunk is placed at the random height
        self.height = random.randrange(50, 400)
        self.top = self.height - self.TOPTRUNK.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, screen):
        screen.blit(self.TOPTRUNK, (self.x, self.top))
        screen.blit(self.BOTTOMTRUNK, (self.x, self.bottom))
        self.hitboxtop = (self.x + 80, self.top, 80, 490)
        self.hitboxbottom = (self.x + 80, self.bottom + 10, 80, 490)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitboxtop, 2)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitboxbottom, 2)


class Honey:
    VEL = 7.5
    BONUS = HONEY

    def __init__(self):
        # appearing randomly
        self.y = random.randrange(100, 500)
        self.x = random.randrange(280, 450)
        self.passed = False
        self.hitbox = (self.x + 10, self.y + 15, 55, 40)

    def move(self):
        self.x -= self.VEL

    def draw(self, screen):
        screen.blit(self.BONUS, (self.x, self.y))
        self.hitbox = (self.x + 10, self.y + 15, 55, 40)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)


def draw_window(screen, bee, ground, trunks, honeys, score, bonus):
    screen.blit(BG, (0, 0))
    text = SCOREFONT.render("Score: " + str(score), True, Green)
    screen.blit(text, (390, 10))
    bonustxt = BONUSFONT.render("Collected bonuses: " + str(bonus), True, Green)
    screen.blit(bonustxt, (10, 10))
    for trunk in trunks:
        trunk.draw(screen)
    for honey in honeys:
        honey.draw(screen)

    bee.draw(screen)
    ground.draw(screen)
    pygame.display.update()


def main():
    bee = Bee(-15, -100)
    ground = Ground(450)
    trunks = [Trunk(400)]
    honeys = [Honey()]

    run = True
    score = 0
    bonus = 0

    # main loop of the game
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bee.jump()

        draw_window(screen, bee, ground, trunks, honeys, score, bonus)

        add_trunk = False
        rem = []
        for trunk in trunks:

            if trunk.x + trunk.TOPTRUNK.get_width() < 0:
                rem.append(trunk)

            if not trunk.passed and trunk.x < bee.x:
                trunk.passed = True
                add_trunk = True

            trunk.move()

            # bee and the trunks collision
            # hitting trunks from the front
            if trunk.hitboxtop[1] < bee.hitbox[1] < trunk.hitboxtop[1] + trunk.hitboxtop[3]:
                if bee.hitbox[0] + bee.hitbox[2] < trunk.hitboxtop[0] + trunk.hitboxtop[2]:
                    if trunk.hitboxtop[0] - bee.hitbox[0] < bee.hitbox[2]:
                        FOREST.stop()
                        PUNCH.play()
                        bee.hit(score)
            if trunk.hitboxbottom[1] < bee.hitbox[1] < trunk.hitboxbottom[1] + trunk.hitboxbottom[3]:
                if bee.hitbox[0] + bee.hitbox[2] < trunk.hitboxbottom[0] + trunk.hitboxbottom[2]:
                    if trunk.hitboxbottom[0] - bee.hitbox[0] < bee.hitbox[2]:
                        FOREST.stop()
                        PUNCH.play()
                        bee.hit(score)

            # collision while being between the trunks
            if trunk.hitboxtop[0] < bee.hitbox[0] < trunk.hitboxtop[0] + trunk.hitboxtop[2]:
                if bee.hitbox[1] - trunk.hitboxtop[1] < trunk.hitboxtop[3]:
                    FOREST.stop()
                    PUNCH.play()
                    bee.hit(score)
            if trunk.hitboxbottom[0] < bee.hitbox[0] < trunk.hitboxbottom[0] + trunk.hitboxbottom[2]:
                if trunk.hitboxbottom[1] - bee.hitbox[1] < bee.hitbox[3]:
                    FOREST.stop()
                    PUNCH.play()
                    bee.hit(score)

        if add_trunk:
            # adding a point if trunk passed
            score += 1
            trunks.append(Trunk(400))

        for r in rem:
            trunks.remove(r)

        ground.move()
        bee.move()

        # bee and the ground collision
        if ground.hitbox1[1] - (bee.hitbox[1] + bee.hitbox[3]) < 0:
            FOREST.stop()
            PUNCH.play()
            bee.hit(score)
        if ground.hitbox2[1] - (bee.hitbox[1] + bee.hitbox[3]) < 0:
            FOREST.stop()
            PUNCH.play()
            bee.hit(score)

        add_bonus = False
        remove = []

        hit_honey = False
        for honey in honeys:
            if not honey.passed and honey.x < bee.x:
                honey.passed = True
                add_bonus = True

            honey.move()

            # hitting honey from the front
            if honey.hitbox[1] < bee.hitbox[1] < honey.hitbox[1] + honey.hitbox[3]:
                if honey.hitbox[0] < bee.hitbox[0] < honey.hitbox[0] + honey.hitbox[2]:
                    BUZZ.play()
                    honeys.remove(honey)
                    hit_honey = True

            elif honey.hitbox[0] < bee.hitbox[0] < honey.hitbox[0] + honey.hitbox[2]:
                # hitting honey from the bottom
                if honey.hitbox[1] < bee.hitbox[1] < honey.hitbox[1] + honey.hitbox[3]:
                    BUZZ.play()
                    honeys.remove(honey)
                    hit_honey = True

                # hitting honey from the top
                if honey.hitbox[1] < bee.hitbox[1] + bee.hitbox[3] < honey.hitbox[1] + honey.hitbox[3]:
                    BUZZ.play()
                    honeys.remove(honey)
                    hit_honey = True
                    if honey.x < bee.x:
                        honey.passed = True
                        add_bonus = True

        for r in remove:
            honeys.remove(r)

        if hit_honey is True:
            # bonus points after hitting honey
            score += 3
            bonus += 1
            add_bonus = True

        if add_bonus:
            honeys.append(Honey())

        pygame.display.update()


def start():
    display = 'intro'

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    # repeating forest music
                    FOREST.play(-1)
                    main()
                if event.key == pygame.K_2:
                    sys.exit()

        if display == 'intro':
            screen.fill(DarkGreen)
            logo()
            title('Welcome to FLAPPYBEE!!!', 40, 100, 20)
            time.sleep(3)
            screen.fill(DarkBlue)
        display = 'menu'
        if display == 'menu':
            menu1("1. PLAY   2. Exit", 40, 100, 20)
            menu("ENTER THE NUMBER FROM THE KEYBOARD", 40, 100, 20)
        elif display == "game":
            pygame.display.update()


start()
