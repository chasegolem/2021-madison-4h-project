from gpiozero import Button
import scrollphathd as sphd
import os

def pressed(button):
    global splash_origin, splash_time
    button_name, x, y = button_map[button.pin.number]
    print("Button {button_name} pressed!")


button_map = {5: ("A", 0, 0),    # Top Left
              6: ("B", 0, 6),    # Bottom Left
              16: ("X", 16, 0),  # Top Rights
              24: ("Y", 16, 7)}  # Bottom Right

button_a = Button(5)
button_b = Button(6)
button_x = Button(16)
button_y = Button(24)