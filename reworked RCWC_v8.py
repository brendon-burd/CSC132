import pygame
import RPi.GPIO as GPIO
from time import sleep

#create a list with all of the pictures for the sprites
walkRight = [pygame.image.load('girl2.png'), pygame.image.load('girl2.png'), pygame.image.load('girl2.png'), pygame.image.load('girl2.png'),\
             pygame.image.load('girl2.png'), pygame.image.load('girl2.png'), pygame.image.load('girl2.png'), pygame.image.load('girl.gif'),\
             pygame.image.load('girl2.png')]
walkLeft = [pygame.image.load('girl2.png'), pygame.image.load('girl2.png'), pygame.image.load('girl2.png'), pygame.image.load('girl2.png'),\
             pygame.image.load('girl2.png'), pygame.image.load('girl2.png'), pygame.image.load('girl2.png'), pygame.image.load('girl2.png'),\
             pygame.image.load('girl2.png')]
walkUp = [pygame.image.load('girl2.png'), pygame.image.load('girl2.png'), pygame.image.load('girl2.png'), pygame.image.load('girl2.png'),\
             pygame.image.load('girl2.png'), pygame.image.load('girl2.png'), pygame.image.load('girl2.png'), pygame.image.load('girl2.png'),\
             pygame.image.load('girl2.png')]
walkDown = [pygame.image.load('girl2.png'), pygame.image.load('girl2.png'), pygame.image.load('girl2.png'), pygame.image.load('girl2.png'),\
             pygame.image.load('girl2.png'), pygame.image.load('girl2.png'), pygame.image.load('girl2.png'), pygame.image.load('girl2.png'),\
             pygame.image.load('girl2.png')]
bg = pygame.image.load('flooring2_V2.png')
key = pygame.image.load('key.png')
char = pygame.image.load('girl2.png')

clock = pygame.time.Clock()
screen = pygame.display.set_mode([800,700])

#set sprite variables
x = 50
y = 50
width = 64
height = 64
vel = 5
        

#define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

#the buttons pin 
UP_BUTT = 19
DOWN_BUTT = 17
R_BUTT = 18
L_BUTT = 16
buttons = [19, 17, 18, 16]

#define the directions
left = False
right = False
up = False
down = False
walkCount = 0

#set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttons, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#class that creates the walls
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)

        #make a wall
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        #make the top-left corner the passed-in location
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        
#class that draws the background and the sprites 
def redrawGameWindow():
    global walkCount
    
    #create the rooms
    rooms = []
    room = TutorialRoom()
    rooms.append(room)

    #create and display the current room
    current_room_num = 0
    current_room = rooms[current_room_num]
    screen.blit(bg, (0,0))
    current_room.wall_list.draw(screen)

    #draw and display the sprite
    if walkCount + 1 >= 60:
        walkCount = 0

    if left:
        screen.blit(walkLeft[walkCount//3], (x,y))
        walkCount += 1
    elif right:
        screen.blit(walkRight[walkCount//3], (x,y))
        walkCount += 1
    elif up:
        screen.blit(walkUp[walkCount//3], (x,y))
        walkCount += 1
    elif right:
        screen.blit(walkDown[walkCount//3], (x,y))
        walkCount += 1
    else:
        screen.blit(char, (x,y))
        
    pygame.display.update()
    
    

#class that creates a key object
class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
    

        #make the base of the object
        self.image = pygame.Surface([24, 30])
        self.image.fill(BLACK)
        #background = pygame.image.load('key.png')
        #screen.blit(background, (0,0))

        #maek the top-left corner the passed-in location
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

#class that creates the player's sprite
#we don't really need this class anymore but I left it in for now -Cam
class Sprite(pygame.sprite.Sprite):
    #initialize the speed
    speed_x = 0
    speed_y = 0

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20,20])  
        self.image.fill(PURPLE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    #change the speed of the sprite 
    def speed(self, x, y):
       self.change_x += x
       self.change_y += y

    #for movment
    def moveUp(self):
        self.rect.y += -4
    def moveDown(self):
        self.rect.y += 4
    def moveLeft(self):
        self.rect.x += -4
    def moveRight(self):
        self.rect.x += 4

#Base class for all rooms
class Room(object):

    # Each room has a list of walls, and of enemy sprites.
    wall_list = None
    key_list = None
    grabbables = None 

    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.grabbables = pygame.sprite.Group()

    #Loop through the list, create the wall, and add it to the list
    def buildWalls(self, walls):
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

    def buildKeys(self, keys):
        for item in keys:
            key = Key(item[0], item[1])
            self.grabbables.add(key)

#########create the rooms#############

class TutorialRoom(Room):
    def __init__(self):
        Room.__init__(self)

        #The list of exterior walls (white) and maze walls (blue)
        walls = [[0, 0, 20, 250, WHITE],
                [0, 350, 20, 250, WHITE],
                [780, 0, 20, 250, WHITE],
                [780, 350, 20, 250, WHITE],
                [20, 0, 760, 20, WHITE],
                [20, 580, 760, 20, WHITE],
                [390, 50, 20, 350, BLUE],
                [360, 50, 420, 20, BLUE],
                [100, 50, 300, 20, BLUE],
                [100, 120, 240, 20, BLUE],
                [100, 130, 20, 500, BLUE],
                [230, 200, 20, 120, BLUE],
                [300, 140, 20, 120, BLUE],
                [230, 310, 180, 20, BLUE],
                [170, 200, 60, 20, BLUE],
                [170, 200, 20, 130, BLUE],
                [170, 200, 20, 200, BLUE],
                [470, 130, 20, 280, BLUE],
                [540, 130, 240, 20, BLUE],
                [540, 130, 20, 140, BLUE],
                [540, 320, 20, 100, BLUE],
                [470, 400, 80, 20, BLUE],
                [540, 320, 100, 20, BLUE],
                [540, 250, 50, 20, BLUE],
                [580, 190, 20, 80, BLUE],
                [580, 190, 200, 20, BLUE],
                [630, 300, 20, 200, BLUE],
                [630, 285, 100, 20, BLUE],
                [750, 200, 20, 35, BLUE],
                [300, 330, 20, 80, BLUE]]
        
        keys = [[760,30]]

        #send walls to build wall function
        Room.buildWalls(self, walls)
        Room.buildKeys(self, keys)


##############main part of the program#######################
def main():
    pygame.init()

    #create a 800x700 screen
    #screen = pygame.display.set_mode([800,700])

    #the title of the window and set the background
    pygame.display.set_caption('Game')

    # Create the sprite object
    player = Sprite(50, 50)
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player) 

    #create a list to call each room
    rooms = []
    room = TutorialRoom()
    rooms.append(room)

    current_room_num = 0
    current_room = rooms[current_room_num]

    done = False

    while not done:

        clock.tick(60)

        pressed = False
        while(not pressed):
            for i in range(len(buttons)):
                while(GPIO.input(buttons[i]) == True):
                    val = i
                    pressed = True

                    if(buttons[val] == UP_BUTT):
                        player.moveUp()
                        left = False
                        right = False
                        up = True
                        down = False
                    elif(buttons[val] == DOWN_BUTT):
                        player.moveDown()
                        left = False
                        right = False
                        up = False
                        down = True
                    elif(buttons[val] == R_BUTT):
                        player.moveRight()
                        left = False
                        right = True
                        up = False
                        down = False
                    elif(buttons[val] == L_BUTT):
                        player.moveLeft()
                        left = True
                        right = False
                        up = False
                        down = False
                    else:
                        left = False
                        right = False
                        up = False
                        down = False
                        walkCount = 0 

                    #Event Processing
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pressed = True
                            done = True

                    #see if player sprite is at the exit
                    if(player.rect.x >= 800):
                        current_room_num += 1
                        player.rect.x = 20

                    #update room
                    current_room = rooms[current_room_num]

                redrawGameWindow()

            pygame.display.flip()

        #clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()





















