# Written by Chase Golem
# Last edited 26 July 2020
# IP release on screen, SSH

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import subprocess
import time
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
font = ImageFont.load_default()
width, height = 17, 7

connected = False

disp.begin()

while connected == False:
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )

    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    padding = -2
    top = padding
    bottom = height-padding
    x = 0
    draw.text((x, top+10),    "IP: " + str(IP),  font=font, fill=255)
    draw.text((x, top+20),    str("Waiting for connection..."),  font=font, fill=255)

    disp.image(image)
    disp.display()
    time.sleep(.01)

    if "SSH_CONNECTION" in os.environ:
        connected = True
        disp.clear()
        width = disp.width
        height = disp.height
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        padding = -2
        top = padding
        bottom = height-padding
        x = 0
        draw.text((x, top+15),    "Detected Connection",  font=font, fill=255)

        disp.image(image)
        disp.display()
        break