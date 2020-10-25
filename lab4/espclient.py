from machine import Pin, Timer
import network
import esp32
import socket
import ssl

led_red = Pin(12, Pin.OUT)
led_green = Pin(21, Pin.OUT)
led_red.value(1)
led_green.value(1)

timer = Timer(0)

essid = "ThisLANisyourLAN"
password = "spicy!avocad0"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(essid, password)
while not wlan.isconnected():
    pass
print("Connected!")

api_host = 'api.thingspeak.com'
api_port = 443
api_key = '3ODNWZEY2LM86CTX'
addr = socket.getaddrinfo(api_host, api_port)[0][-1]

def send_data(timer):
    temp = esp32.raw_temperature()
    hall = esp32.hall_sensor()
    print("Temperature: "+str(temp)+", Hall: "+str(hall))
    
    msg = b'GET https://api.thingspeak.com/update?api_key=3ODNWZEY2LM86CTX&field1='+str(temp)    
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    s.sendall(msg)
    s.close()
    
timer.init(period=16000, mode=Timer.PERIODIC, callback=send_data)
