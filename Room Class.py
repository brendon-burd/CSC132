import pygame

#define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

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
        #send walls to buil wall function
        Room.buildWalls(self, walls)
        
    

####### This is the main part of the program ##########
def main():
    pygame.init()

    #create a 800x700 screen
    screen = pygame.display.set_mode([800,700])

    #the title of the window and set the background
    pygame.display.set_caption('Game')
    #background = pygame.image.load('program/tiles2_v3.gif')

    #create the player object

    rooms = []

    room = TutorialRoom()
    rooms.append(room)

    current_room_num = 0
    current_room = rooms[current_room_num]

    clock = pygame.time.Clock()

    done = False

    while not done:
        #Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            #brenden's controls

        #Game logic
        #also brenden's controls
 
        #drawing the backgrounds
        background = pygame.image.load('tiles2_v3.gif')
        screen.fill(BLACK)
        screen.blit(background, (0,0))
        
        
        current_room.wall_list.draw(screen)
 
        pygame.display.flip()
 
        clock.tick(60)
 
    pygame.quit()

if __name__ == "__main__":
    main()

        































    
