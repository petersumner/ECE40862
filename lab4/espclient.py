from machine import Pin, Timer
import network
import esp32
import socket
import ssl

# Initialize Red and Green LEDS on GPIO Output
led_red = Pin(12, Pin.OUT)
led_green = Pin(21, Pin.OUT)
led_red.value(1)
led_green.value(1)


timer = Timer(0)

# Connect to WiFi network
essid = "The MATRIX"
password = "redacted"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(essid, password)
while not wlan.isconnected():
    pass
print("Connected!")
print(wlan.ifconfig())

# Connect to ThingSpeak
api_key = '3ODNWZEY2LM86CTX'
ai = socket.getaddrinfo('api.thingspeak.com', 80)[0][-1]
addr = [(2, 1, 0, '', ('10.0.0.158', 80))][0][-1]

#Send data via API key
def send_data(timer):    
    html = """
    POST /update HTTP/1.1
    Host: api.thingspeak.com
    Connection: close
    X-THINGSPEAKAPIKEY: 3ODNWZEY2LM86CTX
    Content-Type: application/x-www-form-urlencoded
    Content-Length: %d
    %s
    """
    temp = esp32.raw_temperature()
    hall = esp32.hall_sensor()
    print('Temperature: '+str(temp)+', Hall: '+str(hall))
    s = socket.socket()
    s.connect(addr)
    s = ssl.wrap_socket(s)
    data = 'field1=%.2f&field2=%.2f' % (temp, hall)
    http = html & (len(data), data)
    s.write(http.encode())
    s.close()

timer.init(period=16000, mode=Timer.PERIODIC, callback=send_data)
