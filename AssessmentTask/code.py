#!/usr/bin/env pybricks-micropython
import sys
import time
import math
import random
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import select

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

#Initialise motors
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

ev3 = EV3Brick()

# Define the keys for manual control
FRONT_KEY = 'w'
BACK_KEY = 's'
LEFT_KEY = 'a'
RIGHT_KEY = 'd'
STOP_KEY = 'm'
AUTOMATIC_KEY = "q"

turn = 1
Manual = 0

obstacle_sensor = UltrasonicSensor(Port.S4)  # Ultrasonic sensor
color_sensor = ColorSensor(Port.S3)  # Color sensor
color_sensor2 = ColorSensor(Port.S1)  # Colour sensor 2

# Initialise the robot
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=118)

# Playing the start 'beep sound''
ev3.speaker.beep()
print("Starting program...")
user_message = ''

# Function to get user input for the message to be displayed when the robot detects green
def get_user_message():
    ev3.screen.clear()
    ev3.screen.print("Enter message:")
    print("Please type the message for Green detection and press Enter:")
    user_message = input()

# function to check for the line or the green block
def checkforobstacles():
    '''
    Checks the secondary color sensor for black objects.
    Stops robot, displays message and beeps if object detected,
    then drives backward. Otherwise shows 'No Obstacles Detected'.
    '''
    if color_sensor2.color() == Color.BLACK:
        robot.stop()
        ev3.screen.clear()
        ev3.screen.print("Object detected!")
        wait(1000)
        ev3.speaker.beep()
        wait(100)
        ev3.speaker.beep()
        wait(100)
        ev3.screen.clear()
        robot.drive_time(-250, 0, 1000)
    else:
        if color_sensor.color() == Color.GREEN:
            robot.stop()
            user_message = get_user_message()
            ev3.screen.clear()
            ev3.screen.print(user_message)
            quit() # Exit the loop when the user message is displayed (Job finished)
        ev3.screen.print("No Obstacles Detected")
        wait(500)
        ev3.screen.clear()

#asks for the user message at the start
get_user_message()

print("Click Q to make it Autonomous")

#main loop
while True:
    time.sleep(0.1)
    print(Manual)
    char = sys.stdin.read(1)
    
    #manual mode
    #checks for which key is pressed and takes action

    if Manual == 0:
        if char == FRONT_KEY:
            ev3.screen.print("Going Forwards")
            robot.drive_time(200, 0, 1000)
            ev3.screen.clear()
            robot.stop()
            checkforobstacles()
            char = " "
        elif char == BACK_KEY:
            ev3.screen.print("Going Backwards")
            robot.drive_time(-200, 0, 1000)
            ev3.screen.clear()
            robot.stop()
            checkforobstacles()
            char = " "
        elif char == LEFT_KEY:
            ev3.screen.print("Turning Left")
            robot.turn(-50)
            ev3.screen.clear()
            robot.stop()
            checkforobstacles()
            char = " "
        elif char == RIGHT_KEY:
            ev3.screen.print("Turning Right")
            robot.turn(50)
            ev3.screen.clear()
            robot.stop()
            checkforobstacles()
            char = " "
        elif char == AUTOMATIC_KEY:
            #switch to automatic mode
            robot.stop()
            ev3.screen.print("Loading Autonomous Mode. . .")
            print("Loading Autonomous Mode. . .")
            Manual = 1
            print("Autoomatic")
        time.sleep(0.1)
    
    #automatic mode

    if Manual == 1:
        ev3.screen.clear()
        ev3.screen.print("Autonomous")
        robot.drive_time(100, 0, 1000)

        # If obstacle (black line) detected, turn randomly left or right
        if color_sensor2.color() == Color.BLACK:
            turn = random.randint(1, 2)
            if turn == 1:
                robot.turn(100) # I use turn 100 instead of 90 because 'turning 90 degrees' turns the robot approx. 75 degrees
                robot.drive_time(100, 0, 1000)
                robot.turn(100)
            if turn == 2:
                robot.turn(-100)
                robot.drive_time(100, 0, 1000)
                robot.turn(-100)

        # Avoiding colours such as red, yellow and blue
        if color_sensor.color() == Color.RED or color_sensor.color() == Color.YELLOW or color_sensor.color() == Color.BLUE:
            robot.stop()
            robot.turn(100)
            robot.drive_time(100, 0, 1000)
            robot.turn(-100)
            robot.drive_time(100, 0, 1000)
            robot.turn(-100)

        # When green is detected, turn and display the user message
        if color_sensor.color() == Color.GREEN:
            robot.turn(-100)
            robot.turn(-100)
            robot.turn(-100)
            robot.turn(-100) #4 turns to make a 360 degree turn (remeber that 100 degree turm is actually 90 degrees))
            robot.stop()
            ev3.screen.clear()
            ev3.screen.print(user_message)
            break # Exit the loop when the user message is displayed (Job finished)
        
        # return back to manual mode if 'm' is pressed
        if char == STOP_KEY:
            robot.stop()
            ev3.screen.print("Loading Manual Mode . . .")
            print("Loading Manual Mode. . .")
            print("Manual Mode Successful")
            Manual = 0