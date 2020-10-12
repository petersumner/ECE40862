import machine
import time

# Accept user time input to initialize real time clock (RTC)
year = int(input("Year? "))
month = int(input("Month? "))
day = int(input("Day? "))
weekday = int(input("Weekday? "))
hour = int(input("Hour? "))
minute = int(input("Minute? "))
second = int(input("Second? "))
micro = int(input("Microseconds? "))

rtc = machine.RTC()
rtc.init((year, month, day, hour, minute, second, micro, 0))

# Initialize three hardware timers
timer = machine.Timer(0)
timer2 = machine.Timer(1)
timer3 = machine.Timer(2)

# External push button switch configured as GPIO (digital) input
switch = machine.Pin(21, machine.Pin.IN)

# External LEDs configured as PWM outputs
led_red = machine.PWM(machine.Pin(14))
led_green = machine.PWM(machine.Pin(15))
led_red.duty(256)
led_green.duty(256)
led_red.freq(10)
led_green.freq(10)

# Initialize external potentiometer as analog input
pot = machine.ADC(machine.Pin(34))
pot.atten(machine.ADC.ATTN_11DB)
pot_value = pot.read()

# LEDs initialized with duty cycle = 256 and frequency = 10Hz
# Button press gives control to potentiometer
# 1st state: RED LED's frequency controlled by pot readings
# 2nd state: GREEN LED's duty cycle controlled by pot readings
# Button press switches between these two states

state = 0

def tick(timer):
    print(rtc.datetime())

def tick2(timer):
    global pot, state
    pot_value = pot.read()
    if state == 1:
        led_red.freq(int(pot_value/100))
    elif state == 2:
        led_green.duty(int(pot_value/8))
        led_red.duty(256)
    
def switch_interrupt(pin):
    global state
    if state == 2 or state == 0:
        state = 1
    elif state == 1:
        state = 2
    
def debounce(pin):
    timer3.init(mode=machine.Timer.ONE_SHOT, period=200, callback=switch_interrupt)
    
timer.init(period=30000, mode=machine.Timer.PERIODIC, callback=tick)
timer2.init(period=1000, mode=machine.Timer.PERIODIC, callback=tick2)
switch.irq(trigger=machine.Pin.IRQ_RISING, handler=debounce)
        