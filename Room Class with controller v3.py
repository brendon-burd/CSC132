import pygame
import RPi.GPIO as GPIO
from time import sleep

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

        #maek the top-left corner the passed-in location
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

#Emily's player class
#class that creates the player's sprite
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

        #there needs to be a peramter that stops the sprite stops when it hits a wall 

#Base class for all rooms
class Room(object):

    # Each room has a list of walls, and of enemy sprites.
    wall_list = None
    enemy_list = None
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

class TutorialRoom(Room):
    def __init__(self):
        Room.__init__(self)

        #The list of walls
        walls = [[0, 0, 20, 250, WHITE],
                [0, 350, 20, 250, WHITE],
                [780, 0, 20, 250, WHITE],
                [780, 350, 20, 250, WHITE],
                [20, 0, 760, 20, WHITE],
                [20, 580, 760, 20, WHITE]]

        #send walls to build wall function
        Room.buildWalls(self, walls)


class Room1(Room):
    def __init__(self):
        Room.__init__(self)

        #The list of walls
        walls = [[0, 0, 20, 250, BLACK],
                [0, 350, 20, 250, BLACK],
                [780, 0, 20, 250, BLACK],
                [780, 350, 20, 250, BLACK],
                [20, 0, 760, 20, BLACK],
                [20, 580, 760, 20, BLACK]]

        #send walls to build wall function
        Room.buildWalls(self, walls)     


####### This is the main part of the program ##########
def main():
    pygame.init()

    #create a 800x700 screen
    screen = pygame.display.set_mode([800,700])

    #the title of the window and set the background
    pygame.display.set_caption('Game')

    # Create the sprite object
    player = Sprite(50, 50)
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player) 

    rooms = []

    room = TutorialRoom()
    rooms.append(room)

    room = Room1()
    rooms.append(room) 

    current_room_num = 0
    current_room = rooms[current_room_num]

    clock = pygame.time.Clock()

    done = False

    while not done:

        pressed = False
        while(not pressed):
            for i in range(len(buttons)):
                while(GPIO.input(buttons[i]) == True):
                    val = i
                    pressed = True

                    if(buttons[val] == UP_BUTT):
                        player.moveUp()
                    elif(buttons[val] == DOWN_BUTT):
                        player.moveDown()
                    elif(buttons[val] == R_BUTT):
                        player.moveRight()
                    elif(buttons[val] == L_BUTT):
                        player.moveLeft()

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


                    #drawing the backgrounds
                    background = pygame.image.load('tiles2_v3.gif')
                    screen.fill(BLACK)
                    screen.blit(background, (0,0))

                    #draw the sprite
                    movingsprites.draw(screen)

                    #draw the walls 
                    current_room.wall_list.draw(screen)

                    pygame.display.flip()

                    clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
