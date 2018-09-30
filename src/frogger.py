import pygame
from pygame.locals import *
import random
import copy

# this is the image we will use for the background
img = pygame.image.load('frogger_board.png')

# Row height
ROW_HEIGHT = 60
# Row that frogger starts on
INIT_ROW = 11
# Finish row, which is where the level ends - row 0 is the score
FINISH_ROW = 1

# WATER ROWS
waterRows = [2, 3, 4, 5]

UP = 0
RIGHT = -90
LEFT = 90
DOWN = 180

screenWidth, screenHeight = 600, 720

pygame.init()

# se the title of the app
pygame.display.set_caption('frogger')


#############################################
#############FROGGER CLASS###################
#############################################
class Frogger(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image = pygame.image.load('frog1.png')
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 240, 660
        self.isDead = False
        self.score = 0

        self.frog_stop = pygame.image.load('frog1.png')

        self.ride = None
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y

    def getCurrentRow(self):
        return self.rect.topleft[1] / ROW_HEIGHT


    def getCurrentX(self):
        return self.rect.topleft[0]

    def move(self, dir):
        self.image = pygame.transform.rotate(self.frog_stop, dir)
        if dir == UP and self.getCurrentRow() != FINISH_ROW:
            self.rect.centery -= ROW_HEIGHT
            self.ride = None
        elif dir == RIGHT and self.getCurrentX() != 540:
            self.rect.centerx += ROW_HEIGHT
            self.ride = None
            print self.rect.topleft
        elif dir == LEFT and self.getCurrentX() != 0:
            self.rect.centerx -= ROW_HEIGHT
            self.ride = None
        elif dir == DOWN and self.getCurrentRow() != INIT_ROW:
            self.rect.centery += ROW_HEIGHT
            self.ride = None

    def update(self):
        if self.isDead is False:
            if self.getCurrentRow() in waterRows and self.ride == None:
                self.dead()

            if self.getCurrentRow() is FINISH_ROW:
                self.reset()
                self.score += 1


            if self.ride != None:
                self.rect.centerx = self.ride.rect.centerx

            if self.rect.centerx < -1 or self.rect.centerx > screenWidth:
                self.dead()





    def dead(self):
        self.image = pygame.image.load('frog_dead.png')
        self.isDead = True
        self.score = 0

    def reset(self):
        # put the frog back to the starting position
        self.rect.topleft = 240, 660
        # change the image back to the living frog
        self.image = self.frog_stop
        # reset the boolean
        self.isDead = False


class Log(pygame.sprite.Sprite):
    def __init__(self, row, direction, initialX, speed):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('log_sm.png')

        self.initialX = initialX
        self.rect= self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 0 + self.initialX, ROW_HEIGHT * row
        self.speed = speed
        self.direction = direction

    def getCurrentX(self):
        return self.rect.topleft[0]

    def update(self):
        self.rect.centerx += self.speed * (self.direction)
        print self.rect.centerx
        if self.getCurrentX() >= (600 + self.rect.width) and self.direction == 1:
            self.rect.centerx = 0 - self.rect.width
        elif self.getCurrentX() <= (0 - self.rect.width) and self.direction == -1:
            self.rect.centerx = 600 + self.rect.width

class Turtle(pygame.sprite.Sprite):
    def __init__(self,row,direction,initialX,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('turtules.png')
        self.initialX = initialX
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 0 + self.initialX, ROW_HEIGHT * row

        self.speed = speed
        self.direction = direction

    def getCurrentX(self):
        return self.rect.topleft[0]

    def update(self):
        self.rect.centerx += self.speed * (self.direction)
        print self.rect.centerx
        if self.getCurrentX() >= (600 + self.rect.width) and self.direction == 1:
            self.rect.centerx = 0 - self.rect.width
        elif self.getCurrentX() <= (0 - self.rect.width) and self.direction == -1:
            self.rect.centerx = 600 + self.rect.width


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, type, row, direction, initialX, speed):
        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer

        if type == 0:
            self.image = pygame.image.load('car.png')
        elif type == 1:
            self.image = pygame.image.load('sportscar.png')
        elif type == 2:
            self.image = pygame.image.load('truck.png')

        self.initialX = initialX
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 0 + self.initialX, ROW_HEIGHT * row

        self.speed = speed
        self.direction = direction

    def getCurrentX(self):
        return self.rect.topleft[0]

    def update(self):
        self.rect.centerx += self.speed * (self.direction)
        print self.rect.centerx
        if self.getCurrentX() >= (600 + self.rect.width) and self.direction == 1:
            self.rect.centerx = 0 - self.rect.width
        elif self.getCurrentX() <= (0 - self.rect.width) and self.direction == -1:
            self.rect.centerx = 600 + self.rect.width
        #if frog.score == 0:
           #self.speed += 1


######################################################
##################HELPER FUNCTIONS####################
######################################################
def checkCollisions():
    for vehicle in vehicles:
        col = pygame.sprite.collide_rect(frog, vehicle)
        if col == True:
            frog.dead()
    for log in logs:
        col = pygame.sprite.collide_rect(frog, log)
        if col == True:
            frog.ride = log
    for turtle in turtles:
        col = pygame.sprite.collide_rect(frog, turtle)
        if col == True:
            frog.ride = turtle


# displays the score in the top row of the game board
def showScore():
    font = pygame.font.Font(None, 40)
    text = font.render(('SCORE:' + str(frog.score)), 1, (255, 255, 0))
    screen.blit(text, (10, 20))


def handleMovement(event):
    if not frog.isDead:
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                frog.move(UP)
            elif event.key == K_LEFT:
                frog.move(LEFT)
            elif event.key == K_RIGHT:
                frog.move(RIGHT)
            elif event.key == K_DOWN:
                frog.move(DOWN)
    elif event.type == pygame.KEYDOWN and event.key == K_r:
        frog.reset()


#######################################################
######################GAME OBJECTS#####################
#######################################################
screen = pygame.display.set_mode((screenWidth, screenHeight))

# the frog!
frog = Frogger()

vehicles = []
car = Vehicle(0, 10, 1, 0, 5)
vehicles.append(car)

car2 = Vehicle(0, 10, 1, -200, 5)
vehicles.append(car2)
truck = Vehicle(2, 9, -1, 600, 2)
vehicles.append(truck)
truck2 = Vehicle(2, 9, -1, 840, 2)
vehicles.append(truck2)
fastcar = Vehicle(1, 8, 1, 0, 10)
vehicles.append(fastcar)
fastcar2 = Vehicle(1,8,1,400,10)
vehicles.append(fastcar2)
truck3 = Vehicle(2,7,-1,800,2)
vehicles.append(truck3)
car3 = Vehicle(0,7,-1,0,2)
vehicles.append(car3)
#vehicle : type,row,direction,initalX,speed
#log + turtle: row,direction,initialX,speed
logs = []

log = Log(2, 1, 0, 5)
logs.append(log)
log2 = Log(4, 1, 0, 2)
logs.append(log2)
log3 = Log(2,1,400,5)
logs.append(log3)
log4 = Log(4,1, 400, 2)
logs.append(log4)
log5 = Log(2,1,800,5)
logs.append(log5)
log6 = Log(4,1,600,2)
logs.append(log6)

turtles = []

turtle = Turtle(3, 1, 0, 3)
turtles.append(turtle)
turtle2 = Turtle(5, -1, 0, 4)
turtles.append(turtle2)
turtle3 = Turtle(5,-1,400,4)
turtles.append(turtle3)
turtle4 = Turtle(3,1,400,3)
turtles.append(turtle4)
turtle5 = Turtle(3,1,800,3)
turtles.append(turtle5)
allsprites = pygame.sprite.LayeredUpdates(frog, car, car2, car3, truck, truck2,truck3, fastcar,fastcar2, log, log2, turtle2, turtle, turtle3, turtle4, log3, log4,log5, log6,turtle5)
clock = pygame.time.Clock()

#########################################
#########################################
################GAME LOOP################
#########################################
#########################################
while True:

    # draw the game board
    screen.blit(img, (0, 0))
    allsprites.change_layer(frog,0)
    # interrogate the events
    for event in pygame.event.get():
        # check if the event is the X button
        if event.type == pygame.QUIT:
            # if it is quit
            pygame.quit()
            exit(0)
        else:
            handleMovement(event)

    checkCollisions()
    allsprites.update()
    allsprites.draw(screen)

    showScore()

    # flip the buffer to display the updated screen
    pygame.display.flip()
    clock.tick(360)
