# Written by Chase Golem
# Last edited 2 July 2020

# Imports
import signal
import time
import math

import touchphat
from gpiozero import Button
import scrollphathd as sphd

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

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

def drawText(text):
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
    draw.text((x, top+15),    str(text),  font=font, fill=255)
    disp.image(image)
    disp.display()


drawText("Press A to begin.")

@touchphat.on_release('A')
def handle_touch(event):
    started = True
    drawText("ok")
    time.sleep(0.5)
    drawText("wheee")
    while True:
        for x in range(17):
            sphd.clear()
            for y in range(7):
                sphd.set_pixel(x, y, 0.25)
            sphd.show()
            time.sleep(1/17.0)
    
