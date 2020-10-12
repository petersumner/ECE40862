from machine import Pin
from time import sleep

# Onboard RED LED connected to IO_13
led_board = Pin(13, Pin.OUT)

# Toggle LED 5 tiems
for i in range(10):
    led_board.value(not led_board.value())
    sleep(0.5) # 0.5 seconds delay

print("Led blinked 5 times")