from machine import TouchPad, Pin
import network

led_red = Pin(14, Pin.OUT)
led_green = Pin(15, Pin.OUT)

switch1 = Pin(39, Pin.IN)
switch2 = Pin(36, Pin.IN)

touch1 = TouchPad(Pin(12))
touch2 = TouchPad(Pin(13))

essid = "ThisLANisyourLAN"
password = "spicy!avocad0"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(essid, password)

while not wlan.isconnected():
    pass

print("Oh Yes! Get connected\nConnected to " + essid)
macBytes = str(wlan.config('mac'))
print("MAC Address: " + ':'.join('%02x' % ord(b) for b in macBytes))
print("IP Address: " + str(wlan.ifconfig()[0]))

