import RPi.GPIO as GPIO
from time import sleep

def moveUp():
    print "up"

def moveDown():
    print "down"

def moveLeft():
    print"left"

def moveRight():
    print "right"

#the buttons pin 
UP_BUTT = 19
DOWN_BUTT = 17
R_BUTT = 18
L_BUTT = 16
buttons = [19, 17, 18, 16]

#set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttons, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

try:
    #forever loop to see if buttons are pressed 
    while(True):
        pressed = False
        while(not pressed):
            for i in range(len(buttons)):
                while(GPIO.input(buttons[i]) == True):
                    val = i
                    pressed = True
        if(buttons[val] == UP_BUTT):
            moveUp()
        elif(buttons[val] == DOWN_BUTT):
            moveDown()
        elif(buttons[val] == R_BUTT):
            moveRight()
        elif(buttons[val] == L_BUTT):
            moveLeft()


except KeyboardInterrupt:
    GPIO.cleanup()
    print "closing"
