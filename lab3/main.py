from machine import TouchPad, Pin, Timer
import network
import ntptime

led_red = Pin(12, Pin.OUT)
led_green = Pin(13, Pin.OUT)

switch1 = Pin(39, Pin.IN)
switch2 = Pin(36, Pin.IN)

touch1 = TouchPad(Pin(14))
touch2 = TouchPad(Pin(15))

timer_date = Timer(0)
timer_touch = Timer(1)
timer_sleep = Timer(2)

essid = "ThisLANisyourLAN"
password = "spicy!avocad0"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(essid, password)

while not wlan.isconnected():
    print("connecting...")
    pass

macBytes = str(wlan.config('mac'))
print("Oh Yes! Get connected\nConnected to " + essid)
print("MAC Address: " + macBytes)
print("IP Address: " + str(wlan.ifconfig()[0]))

#ntptime.time()

def display_time(timer):
    print("hoohoohaha")
    
def read_touch(timer):
    touch_val1 = touch1.read()
    touch_val2 = touch2.read()
    print(touch_val1, touch_val2)

timer_date.init(period=15000, mode=Timer.PERIODIC, callback=display_time)
timer_touch.init(period=100, mode=Timer.PERIODIC, callback=read_touch)

