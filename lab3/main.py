from machine import TouchPad, Pin, Timer
import network
import ntptime

led_red = Pin(14, Pin.OUT)
led_green = Pin(15, Pin.OUT)

switch1 = Pin(39, Pin.IN)
switch2 = Pin(36, Pin.IN)

touch1 = TouchPad(Pin(12))
touch2 = TouchPad(Pin(13))

timer_date = Timer(0)
timer_touch = Timer(1)
timer_sleep = Timer(2)

essid = "ThePromisedLAN"
password = "fourwordsalluppercase"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(essid, password)

while not wlan.isconnected():
    print("connecting...")
    pass

macBytes = str(wlan.config('mac'))
print("Oh Yes! Get connected\nConnected to " + essid)
print("MAC Address: " + ':'.join('%02x' % ord(b) for b in macBytes))
print("IP Address: " + str(wlan.ifconfig()[0]))

ntptime.settime()
