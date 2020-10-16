from machine import TouchPad, Pin, Timer, deepsleep, RTC
import network
import esp32
import ntptime
import utime

# Initialize external LEDs as GPIO outputs
led_red = Pin(12, Pin.OUT)
led_green = Pin(21, Pin.OUT)
led_red.value(1) # Set RED LED to ON

# Initialize external push button switches as GPIO inputs
switch1 = Pin(4, Pin.IN)
switch2 = Pin(27, Pin.IN)

# Initialize capacitive touchpads
touch1 = TouchPad(Pin(14))
touch2 = TouchPad(Pin(15))
touch1.config(200) # Configure threshold for touchpad 1

# Initialize four hardware timers
timer_date = Timer(0)
timer_touch = Timer(1)
timer_sleep = Timer(2)
timer_wait = Timer(3)

# Connect to WiFi network
essid = "ThisLANisyourLAN"
password = "redacted"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(essid, password)
while not wlan.isconnected():
    print("connecting...")
    pass

# Print connection information
macBytes = str(wlan.config('mac'))
macString = ''
for ch in macBytes[1:]:
    if ch.isdigit() or (ch.isalpha() and ch != 'x'):
        macString += str(ch)
x = iter(macString)
macString = ':'.join(a+b for a,b in zip(x,x))
print("Oh Yes! Get connected\nConnected to " + essid)
print("MAC Address: " + macString)
print("IP Address: " + str(wlan.ifconfig()[0]))

# Initialize real time clock (RTC) using web server
rtc = RTC()
t = ntptime.time()
ntptime.settime()

def display_time(timer):
    date = rtc.datetime()
    month = str(date[1])
    day = str(date[2])
    year = str(date[0])
    hour = date[3] + 4
    minute = date[4]
    second = date[5]
    print('\nDate: ' + month + '/' + day + '/' + year)
    print('Time: ' + '%02d' % hour + ':' + '%02d' % minute + ':' + '%02d' % second + ' HRS')
    
def read_touch(timer):
    touch_val1 = touch1.read()
    touch_val2 = touch2.read()

    # Touching touchpad 2 turns on the GREEN LED
    if touch_val2 < 200:
        led_green.value(1)
    else:
        led_green.value(0)
        
def wake_up(pin):
    # RED LED is on when the board is awake
    led_red.value(1)
    
def activate(timer):
    timer_sleep.init(period=9000, mode=Timer.PERIODIC, callback=set_sleep)

def set_sleep(timer):
    # Board enters deepsleep for 60 seconds
    # Can be woken up by:
    # - touching touchpad 2 (touchpad 1 has no effect)
    # - pressing either of the push button switches
    print("I am awake. Going to sleep for 1 minute.")
    led_red.value(0)
    esp32.wake_on_touch(True)
    esp32.wake_on_ext1(pins=(switch1, switch2), level=esp32.WAKEUP_ANY_HIGH)
    deepsleep(60000)

# Current time is displayed every 15 seconds
timer_date.init(period=15000, mode=Timer.PERIODIC, callback=display_time)

# Reads capacitive touchpad values every 10ms
timer_touch.init(period=100, mode=Timer.PERIODIC, callback=read_touch)

# After 30 seconds, the deepsleep protocol is activated
timer_wait.init(period=30000, mode=Timer.ONE_SHOT, callback=activate)

