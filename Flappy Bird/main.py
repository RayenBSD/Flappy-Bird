import pygame as pg
import time as tm
import random as rand
import os

class Bird:
    #constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y

    #setter
    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y

    #getter
    def getX(self):
        return self.x
    def getY(self):
        return self.y

    #adder
    def addX(self, x):
        self.x += x
    def addY(self, y):
        self.y += y

class Pipe(Bird): pass

pg.init()
screenX, screenY = 640, 680
screen = pg.display.set_mode((screenX, screenY))
icon = pg.image.load(os.path.join("images", "toppng.com-flappy-bird-pixel-art-flappy-bird-630x445.png"))
pg.display.set_icon(icon)
pg.display.set_caption("Flappy Bird")

#Player
flappyBird = Bird(220, 240)
rtt = 0
#Jump
speed = 10
isJumping = False
#Pipe
pipes1 = []
pipes2 = []
pipes1_image = []
pipes2_image = []
number = 5
score = 0
distance = 700

def restart():
    global score, distance
    pipes1.clear()
    pipes2.clear()
    pipes1_image.clear()
    pipes2_image.clear()
    score = 0
    distance = 700
    menu()

def generatePipe(x):
    global pipes1, pipes2, distance, flappyBird, score, speed

    for i in range(number):
        if i > 0:
            rand1 = pipes1[i-1].getX() + 250
        else:
            rand1 = rand.randint(680, 1000)

        if x == 1:
            pipes1.append(Pipe(rand1, rand.randint(-200, -100)))
            pipes2.append(Pipe(pipes1[i].getX(), pipes1[i].getY() + distance))

            pipes1_image.append(pg.transform.rotate(
                pg.transform.scale(
                    pg.image.load(
                        os.path.join("images", "kindpng_2032447.png")),
                            (100, 350)), 180))

            pipes2_image.append(pg.transform.scale(
                pg.image.load(
                    os.path.join("images", "kindpng_2032447.png")),
                        (100, 350)))
        else:
            if pipes1[i].getX() <= -100:

                if i == 0: rand1 = pipes1[number-1].getX() + 250

                pipes1[i].setX(rand1)
                pipes1[i].setY(rand.randint(-200, -100))

                pipes2[i].setX(rand1)
                pipes2[i].setY(pipes1[i].getY() + distance-score)

        if (170 < pipes1[i].getX() < flappyBird.getX() + 40 and pipes1[i].getY() + 350 > flappyBird.getY()):
            tm.sleep(2)
            restart()

        if (170 < pipes2[i].getX() < flappyBird.getX() + 50 and pipes2[i].getY() < flappyBird.getY() + 50):
            tm.sleep(2)
            restart()

        if flappyBird.getX() - 6 < pipes1[i].getX() + 100 < flappyBird.getX(): score += 1

#Game Play
def move():
    global rtt, speed, isJumping, screenY, pipes1, pipes2, pipes2_image, pipes1_image, distance

    keys = pg.key.get_pressed()


    if keys[pg.K_SPACE] and flappyBird.getY() + speed + 50 >= 0:
        isJumping = True
        speed = 10

    if isJumping:
        if speed >= -10:
            neg = 1
            rtt = 45
            if speed < 0:
                rtt = -45
                neg = -1
            flappyBird.addY(-((speed**2)*0.25*neg))
            speed -= 1
        else:
            isJumping = False
            speed = 10
    else:
        rtt = -45
        flappyBird.addY((speed**2)*0.25)

    if flappyBird.getY() >= 500:
        tm.sleep(2)
        restart()

def redraw():
    global pipe1, pipe2, screen, bird, flappyBird, score

    #Back Ground
    backGround = pg.transform.scale(pg.image.load(os.path.join("images", "Flappy bird city background_ Makes a nice wallpaper_.jpg")), (640, 680))

    #bird
    bird = pg.transform.rotate(
        pg.transform.scale(
            pg.image.load(
                os.path.join("images", "toppng.com-flappy-bird-pixel-art-flappy-bird-630x445.png")), (50, 50))
        , rtt)

    #Text
    score_text = pg.font.Font("freesansbold.ttf", 32).render(f"Score: {score}", True, (255, 255, 255))

    #Display
    screen.blit(backGround, (0, 0))
    screen.blit(bird, (flappyBird.getX(), flappyBird.getY()))

    for i in range(number):
        pipes1[i].addX(-5)
        pipes2[i].addX(-5)

        screen.blit(pipes1_image[i], (pipes1[i].getX(), pipes1[i].getY()))
        screen.blit(pipes2_image[i], (pipes2[i].getX(), pipes2[i].getY()))

    screen.blit(score_text, (0, 0))

def main():
    generatePipe(1)
    while True:
        pg.time.Clock().tick(60)

        for events in pg.event.get():
            if events.type == pg.QUIT:
                quit()

        move()
        generatePipe(0)
        redraw()
        pg.display.update()

def menu():
    title = pg.font.SysFont("comicsans", 32)
    while True:
        screen.blit(pg.transform.scale(
            pg.image.load(
                os.path.join(
                    "images", "Flappy bird city background_ Makes a nice wallpaper_.jpg")),
            (640, 680)), (0, 0))
        label = title.render("Press space to begin...", True, (255,255,255))
        screen.blit(label, (screenX/2-label.get_width()/2, 240))
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if pg.key.get_pressed()[pg.K_SPACE]:
                main()

if __name__ == "__main__": menu()