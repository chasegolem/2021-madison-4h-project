# Written by Chase Golem
# Last edited 24 July 2020
# Transmission file, starts game

# Imports
import os
import signal
import time
import math
import engine
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

import subprocess as sp

started = False
engineProcess = False

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

splash_origin = (0, 0)
splash_time = 0
disp.begin()

PID = False

def finished():
    global started
    global engineProcess
    engineProcess.kill()
    started = False
    disp.clear()
    disp.display()
    sphd.clear()
    sphd.show()
    drawMainText()

def drawMainText():
    disp.clear()
    disp.display()
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    padding = -2
    top = padding
    bottom = height-padding
    x = 0
    draw.text((x, top+10),    str("Transmission Mode"),  font=font, fill=255)
    draw.text((x, top+20),    str("Press D to start."),  font=font, fill=255)
    disp.image(image)
    disp.display()

drawMainText()

@touchphat.on_release('D')
def handle_touch(event):
    global started
    global engineProcess
    if started == False:
        started = True
        time.sleep(0.5)
        egn = sp.Popen(['python', '-i', 'engine.py'])
        engineProcess = egn