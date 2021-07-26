# Written by Chase Golem
# Last edited 26 July 2020
# Engine file, main game

# Imports
import signal
import time
import os
import math
import sys
from random import randint

import touchphat
from gpiozero import Button
import scrollphathd as sphd

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import threading

import subprocess

started = False

RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
font = ImageFont.load_default()
sphd.set_brightness(0.5)
width, height = 17, 7

disp.clear()
disp.display()
sphd.clear()
sphd.show()

button_map = {5: ("A", 0, 0),    # Top Left
              6: ("B", 0, 6),    # Bottom Left
              16: ("X", 16, 0),  # Top Right
              24: ("Y", 16, 7)}  # Bottom Right

button_a = Button(5)
button_b = Button(6)
button_x = Button(16)
button_y = Button(24)

splash_origin = (0, 0)
splash_time = 0
disp.begin()

bricks = []

ball = False

def drawText(text):
    disp.clear()
    disp.display()
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    padding = -2
    top = padding
    bottom = height-padding
    x = 0
    draw.text((x, top+15),    str(text),  font=font, fill=255)
    disp.image(image)
    disp.display()

start = 0
end = 5
finished = False

print(start, end)

def drawBricks():
    global bricks
    for b in bricks:
        for a in b:
            sphd.set_pixel(a[1], a[0], 0.5)
            sphd.show()
        time.sleep(0.05)

def calculateBricks():
    global bricks
    global num
    global x
    x = 0
    total = 0
    while total < 15:
        for _ in range(3, 4):
            num = randint(3, 4)
            print(num)
            group = []
            for b in range(total, (total + num)):
                group.append([x, b])
            total += (num + 1)
            bricks.append(group)
            group = []
        if total >= 15:
            total = 0
            x = x + 1
            if x == 3:
                drawBricks()
                break

currentPosition = [2, 4]  # x, y; x starts at 0 -> 16, y starts at 6 -> 0
currentDirection = "up"
horizontalDirection = "right"
ball_started = False

def liveRedraw():
    global finished
    sphd.clear()
    if finished == False:
        sphd.set_pixel(currentPosition[0], currentPosition[1], 1)
    for b in bricks:
        for a in b:
            sphd.set_pixel(a[1], a[0], 0.25)
    for x in range(start, end):
        sphd.set_pixel(x, 6, 0.5)
    sphd.show()
    time.sleep(1/10000000)

def restart():
    global started
    global start
    global end
    global currentPosition
    global currentDirection
    global horizontalDirection
    global bricks
    global ball
    drawText("Press A to begin.")
    bricks.clear()
    sphd.clear()
    sphd.show()
    started = False
    start = 0
    end = 5
    currentPosition = [2, 4]
    currentDirection = "up"
    horizontalDirection = "right"
    ball = threading.Thread(target=startBallMovement)
    ball.start()

def startBallMovement():
    global currentPosition
    global currentDirection
    global horizontalDirection
    global bricks
    global start
    global end
    global finished
    global ball
    sphd.set_pixel(currentPosition[0], currentPosition[1], 1)
    sphd.show()

    print(bricks)

    while True:
        if finished == False:
            if currentDirection == "up":
                if horizontalDirection == "right":
                    currentPosition[0] -= 1  # increasing to right
                    currentPosition[1] -= 1  # increasing to top
                else:
                    currentPosition[0] += 1  # decreasing to left
                    currentPosition[1] -= 1  # increasing to top

                liveRedraw()

                for _ in bricks:
                    for b in _:
                        if [currentPosition[1], currentPosition[0]] == b:
                            print(_, "brick detected")
                            currentDirection = "down"
                            if(horizontalDirection == "right"):
                                horizontalDirection = "left"
                            else:
                                horizontalDirection = "right"
                            bricks.remove(_)
                            for a in _:
                                sphd.set_pixel(a[1], a[0], 0)
                                sphd.show()

                if currentPosition == [0, 0]:
                    currentDirection = "down"
                    horizontalDirection = "right"
                elif currentPosition == [0, 6]:
                    currentDirection = "up"
                    currentPosition = [1, 6]
                else:
                    if currentPosition[1] == 0:
                        currentDirection = "down"
                        if(horizontalDirection == "right"):
                            horizontalDirection = "left"
                        else:
                            horizontalDirection = "right"

                    if currentPosition[0] >= 16:
                        if(horizontalDirection == "right"):
                            horizontalDirection = "left"
                        else:
                            horizontalDirection = "right"

                    if currentPosition[0] == 0:
                        if(horizontalDirection == "right"):
                            horizontalDirection = "left"
                        else:
                            horizontalDirection = "right"
                

            if currentDirection == "down":
                if horizontalDirection == "left":
                    currentPosition[0] -= 1  # decreasing to left
                    currentPosition[1] += 1  # decreasing to bottom
                else:
                    currentPosition[0] += 1  # increasing to right
                    currentPosition[1] += 1  # decreasing to bottom

                for _ in bricks:
                    for b in _:
                        if [currentPosition[1], currentPosition[0]] == b:
                            print(_, "brick detected")
                            currentDirection = "up"
                            if(horizontalDirection == "right"):
                                horizontalDirection = "left"
                            else:
                                horizontalDirection = "right"
                            bricks.remove(_)
                            for a in _:
                                sphd.set_pixel(a[1], a[0], 0)
                                sphd.show()

                liveRedraw()

                print("Current Position (X, Y):",
                    currentPosition[0], currentPosition[1])
                print("Bar Position (Start, End):", start, end)
                print(end > currentPosition[0])
                print(start < currentPosition[0])
                if currentPosition[1] == 6:
                    if end >= currentPosition[0] and start <= currentPosition[0]:
                        if(horizontalDirection == "right"):
                            horizontalDirection = "left"
                        else:
                            horizontalDirection = "right"
                        currentDirection = "up"
                    else:
                        finished = True
                        drawText("Finished. Resetting...")
                        time.sleep(5)
                        restart()
                        break

                if currentPosition == [0, 6]:
                    currentDirection = "up"
                    currentPosition = [1, 6]

                if currentPosition[0] <= 0:
                    horizontalDirection = "right"

                if currentPosition[0] >= 16:
                    horizontalDirection = "left"

            print(currentPosition, currentDirection)
            liveRedraw()
            time.sleep(1)

        if(len(bricks) == 0):
            finished = True
            drawText("All bricks destroyed.")
            time.sleep(0.5)
            drawText("Resetting...")
            time.sleep(0.5)
            restart()
            break

@touchphat.on_release('Back')
def movebar_left(event):
    print("move back")
    global start
    global end
    global bricks
    if start != 0:
        start = start - 1
        end = end - 1
        liveRedraw()
        print('moved')
        print(start, end)


@touchphat.on_release('Enter')
def movebar_right(event):
    print('move forward')
    global start
    global end
    global bricks
    if end != 17:
        start = start + 1
        end = end + 1
        liveRedraw()
        print('moved')
        print(start, end)

drawText("Press A to begin.")

@touchphat.on_release('A')
def handle_touch(event):
    global started
    global ball
    global ball_started
    if started == False:
        started = True
        drawText("Use arrows to move.")
        time.sleep(0.5)
        calculateBricks()
        if ball_started == False:
            ball = threading.Thread(target=startBallMovement)
            ball.start()
            ball_started = True # should rely on 'started' after ball is started, because threading isn't easily stopped