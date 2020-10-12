from machine import Pin
from time import sleep
import sys
    
# Push button switches configured as GPIO inputs
switch1 = Pin(14, Pin.IN)
switch2 = Pin(15, Pin.IN)

# External LEDs configured as GPIO outputs
led_red = Pin(32, Pin.OUT)
led_green = Pin(33, Pin.OUT)

count1, count2 = 0, 0

# LEDs will light when buttons are pressed as per the pattern below
# ----------------------------------------
# Switch1   Switch2   Red_LED   Green_LED
#   OFF       OFF       OFF        OFF
#   OFF       ON        OFF        ON
#   ON        OFF       ON         OFF
#   ON        ON        OFF        OFF
# ----------------------------------------
# Pattern stops and LEDs blink alternatively if one button has been 
# pressed 10 times, program exits when the other button is pressed
while True:
    
    switch1_state = switch1.value()
    switch2_state = switch2.value()
    
    count1 += switch1_state
    count2 += switch2_state

    if switch1_state != 1 or switch2_state != 1:
        led_red.value(switch1_state)
        led_green.value(switch2_state)
    else:
        led_red.value(0)
        led_green.value(0)
    
    while switch1_state == 1 or switch2_state == 1:
        switch1_state = switch1.value()
        switch2_state = switch2.value()
        if switch1_state == 1 and switch2_state == 1:
            led_red.value(0)
            led_green.value(0)
        
    if count1 > 9 or count2 > 9:
        alternate = 0
        while True:
            alternate += 1
            if alternate > 10000:
                led_red.value(not led_red.value())
                led_green.value(not led_green.value())
                alternate = 0
            if (count1 == 10 and switch2.value() == 1) or 
               (count2 == 10 and switch1.value() == 1):
                led_red.value(0)
                led_green.value(0)
                print("You have sucessfully implemented LAB1 DEMO!!!")
                sys.exit()
