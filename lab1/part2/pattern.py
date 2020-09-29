from machine import Pin
from time import sleep
import sys
    
switch1 = Pin(14, Pin.IN)
switch2 = Pin(15, Pin.IN)
led_red = Pin(32, Pin.OUT)
led_green = Pin(33, Pin.OUT)

count1, count2 = 0, 0

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
            if (count1 == 10 and switch2.value() == 1) or (count2 == 10 and switch1.value() == 1):
                led_red.value(0)
                led_green.value(0)
                print("You have sucessfully implemented LAB1 DEMO!!!")
                sys.exit()
