import pygame
import time
import os
import random

pygame.font.init()
STAT_FONT = pygame.font.SysFont("arial", 20)

CRANE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("IMGs", "Crane.png")), (600, 570))
WRECKINGBALL_IMG = pygame.transform.scale(pygame.image.load(os.path.join("IMGs", "WreckingBall.png")), (50, 300))
CLAW_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("IMGs", "Openclaw.png")), (50, 300)),
    pygame.transform.scale(pygame.image.load(os.path.join("IMGs", "Clawwithbrick.png")), (50, 300))]
PILE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("IMGs", "brickpile.png")), (350, 160))
BRICK_IMG = pygame.transform.scale(pygame.image.load(os.path.join("IMGs", "Brick.png")), (30, 20))
FLOOR_IMG = pygame.transform.scale((pygame.image.load(os.path.join("IMGs", "Base.png"))), (600, 30))
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("IMGs", "Background.png")), (600, 600))

class Crane:
    IMG = CRANE_IMG
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def arrive(self):
        self.x += 5

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))

class Pile:
    IMG = PILE_IMG
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def hit(self):
        self.y += 20

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))

class Floor:
    IMG = FLOOR_IMG

    def __init__(self, y):
        self.x = 0
        self.y = y

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))

class WreckingBall:
    IMG = WRECKINGBALL_IMG
    def __init__(self, x, y):
        self.x = x
        self.y1 = y
        self.y2 = y-300
        self.length = 0
        self.xspeed = -30
        self.yspeed = 30
        self.vertical = False
        self.crop1 = 240
        self.crop2 = 540
        self.crop1length = 60
        self.crop2length = -240

    def collide(self, pile):
        if (self.y1 + 300) >= pile.y:
            return True
        else:
            return False
    
    def move(self):
        if self.vertical == False:
            self.x += self.xspeed
            if self.x <= 160:
                self.xspeed = 30
            if self.x >= 550:
                self.xspeed = -30
        if self.vertical == True:
            self.y1 += self.yspeed
            self.y2 += self.yspeed
            if self.yspeed == 30:
                self.crop1 -= 30
                self.crop1length +=30
                self.crop2 -= 30
                self.crop2length +=30
            if self.yspeed ==-30:
                self.crop1 += 30
                self.crop1length -=30
                self.crop2 += 30
                self.crop2length -=30
            if self.y1 <= -199:
                self.yspeed = 30
                self.vertical = False
                self.y1 = -200
                self.y2 = -500

        
    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y1+self.crop1), (0, self.crop1, 50, self.crop1length))
        win.blit(pygame.transform.flip(self.IMG, False, True), (self.x, self.y2+self.crop2), (0, self.crop2, 50, self.crop2length))

class Claw:
    IMGS = CLAW_IMGS

    def __init__(self, x, y):
        self.x = x
        self.y1 = y
        self.y2 = y-300
        self.length = 0
        self.xspeed = -30
        self.yspeed = 30
        self.vertical = False
        self.crop1 = 240
        self.crop2 = 540
        self.crop1length = 60
        self.crop2length = -240
        self.bricks = {160:570, 190:570, 220:570, 250:570, 280:570, 310:570, 340:570, 370:570, 400:570, 430:570, 460:570, 490:570, 520:570, 550:570}

    def move(self):
        if self.vertical == False:
            self.x += self.xspeed
            if self.x <= 160:
                self.xspeed = 30
            if self.x >= 550:
                self.xspeed = -30
        if self.vertical == True:
            self.y1 += self.yspeed
            self.y2 += self.yspeed
            if self.yspeed == 30:
                self.crop1 -= 30
                self.crop1length +=30
                self.crop2 -= 30
                self.crop2length +=30
            if self.yspeed ==-30:
                self.crop1 += 30
                self.crop1length -=30
                self.crop2 += 30
                self.crop2length -=30
            if self.y1 <= -199:
                self.yspeed = 30
                self.vertical = False
                self.y1 = -200
                self.y2 = -500

    def place(self):
        if ((self.y1+300) >= (self.bricks[self.x])) and (self.yspeed != -30):
            self.bricks[self.x] -= 20
            return True
        else:
            return False
                
    def draw(self, win):
        if self.yspeed == 30:
            win.blit(self.IMGS[1], (self.x, self.y1+self.crop1), (0, self.crop1, 50, self.crop1length))
            win.blit(pygame.transform.flip(self.IMGS[1], False, True), (self.x, self.y2+self.crop2), (0, self.crop2, 50, self.crop2length))
        if self.yspeed == -30:
            win.blit(self.IMGS[0], (self.x, self.y1+self.crop1), (0, self.crop1, 50, self.crop1length))
            win.blit(pygame.transform.flip(self.IMGS[0], False, True), (self.x, self.y2+self.crop2), (0, self.crop2, 50, self.crop2length))

class Brick:
    IMG = BRICK_IMG
    def __init__(self, x, y):
        self.xleft = x
        self.ytop = y

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))

        
def draw_window(win, floor, crane, pile, wreckingball, claw, bricks, phase, block_limit, run):
    win.blit(BG_IMG, (0,0))
    crane.draw(win)
    if phase == "start":
        text1 = STAT_FONT.render("Break It Down and Rebuild", 1, (255, 0, 0))
        text2 = STAT_FONT.render("Press space to start.", 1, (255, 0, 0))
        win.blit(text1, (200, 250))
        win.blit(text2, (200, 270))
    if phase == 1:
        wreckingball.draw(win)
        text1 = STAT_FONT.render("Press down to drop the wrecking ball!", 1, (255, 0, 0))
        text2 = STAT_FONT.render("Crush the abandoned tower!", 1, (255, 0, 0))
        win.blit(text1, (60, 10))
        win.blit(text2, (80, 30))
    if (phase == 0) or (phase == 1):
        pile.draw(win)
    if phase == 2:
        text1 = STAT_FONT.render("Now you will build a new tower!", 1, (255, 0, 0))
        text2 = STAT_FONT.render("Press space to continue.", 1, (255, 0, 0))
        win.blit(text1, (175, 250))
        win.blit(text2, (200, 270))
    if phase == 3:
        claw.draw(win)
        for key in bricks.keys():
            for item in bricks[key]:
                win.blit(BRICK_IMG, (key, item))
        text1 = STAT_FONT.render("Blocks left:", 1, (255, 0, 0))
        text2 = STAT_FONT.render(str(block_limit), 1, (255, 0, 0))
        text3 = STAT_FONT.render("Press down to", 1, (255, 0, 0))
        text4 = STAT_FONT.render("place a block.", 1, (255, 0, 0))
        text5 = STAT_FONT.render("Press return to", 1, (255, 0, 0))
        text6 = STAT_FONT.render("end construction.", 1, (255, 0, 0))
        win.blit(text1, (10, 10))
        win.blit(text2, (10, 30))
        win.blit(text3, (10, 200))
        win.blit(text4, (10, 220))
        win.blit(text5, (10, 240))
        win.blit(text6, (10, 260))
    if phase == 4:
        for key in bricks.keys():
            for item in bricks[key]:
                win.blit(BRICK_IMG, (key, item))
        text1 = STAT_FONT.render("Here is your final tower.", 1, (255, 0, 0))
        text2 = STAT_FONT.render("Press space to start a new tower.", 1, (255, 0, 0))
        win.blit(text1, (200, 60))
        win.blit(text2, (175, 80))
    floor.draw(win)
    pygame.display.update()

def main():
    crane = Crane(-600,0)
    floor = Floor(570)
    pile = Pile(210,420)
    wreckingball = WreckingBall(550, -200)
    claw = Claw(550, -200)
    bricks = {160:[570], 190:[570], 220:[570], 250:[570], 280:[570], 310:[570], 340:[570], 370:[570], 400:[570], 430:[570], 460:[570], 490:[570], 520:[570], 550:[570]}
    block_limit = 64
    win = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()

    phase = "start"
    run = True
    while run == True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if phase == "start":
            if keys[pygame.K_SPACE]:
                phase = 0
        if phase == 0:
            crane.arrive()
            if crane.x == 0:
                phase = 1
        if phase == 1:
            wreckingball.move()
            if keys[pygame.K_DOWN]:
                wreckingball.vertical = True
            if wreckingball.collide(pile) == True:
                wreckingball.yspeed = -30
                pile.hit()
            if pile.y >= 570 and wreckingball.y1 <= -200:
                phase = 2
        if phase == 2:
            if keys[pygame.K_SPACE]:
                phase = 3
        if phase == 3:
            claw.move()
            if keys[pygame.K_RETURN]:
                phase = 4
            if keys[pygame.K_DOWN] and len(bricks[claw.x]) < 20:
                claw.vertical = True
            if claw.place() == True:
                claw.yspeed = -30
                bricks[claw.x].append((bricks[claw.x][len(bricks[claw.x])-1])-20)
                block_limit -= 1
            if block_limit == 0 and claw.y1 <= -200:
                phase = 4
        if phase == 4:
            if keys[pygame.K_SPACE]:
                claw = Claw(550, -200)
                bricks = {160:[570], 190:[570], 220:[570], 250:[570], 280:[570], 310:[570], 340:[570], 370:[570], 400:[570], 430:[570], 460:[570], 490:[570], 520:[570], 550:[570]}
                block_limit = 64
                phase = 3
        draw_window(win, floor, crane, pile, wreckingball, claw, bricks, phase, block_limit, run)
    pygame.quit()
    return 
main()