from machine import Pin
import network
import esp32
import esp
import gc
try:
  import usocket as socket
except:
  import socket

esp.osdebug(None)
gc.collect()

ssid = 'ThisLANisyourLAN'
password = 'spicy!avocad0'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while not wlan.isconnected():
  pass
print('Connected!')
print(wlan.ifconfig())

red_led = Pin(12, Pin.OUT)
green_led = Pin(21, Pin.OUT)

switch1 = Pin(4, Pin.OUT)
switch2 = Pin(27, Pin.OUT)

def web_page():
    temp = esp32.raw_temperature()
    hall = esp32.hall_sensor()
    if red_led.value() == 1:
        red_led_state = 'ON'
    else:
        red_led_state = 'OFF'
    if green_led.value() == 1:
        green_led_state = 'ON'
    else:
        green_led_state = 'OFF'
    if switch1.value() == 1:
        switch1_state = 'ON'
    else:
        switch1_state = 'OFF'
    if switch2.value() == 1:
        switch2_state = 'ON'
    else:
        switch2_state = 'OFF'
  
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h1 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h1>ESP32 WEB Server</h1>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
    RED LED Current State: <strong>""" + red_led_state + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p>
    <a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    <p>
    GREEN LED Current State: <strong>""" + green_led_state + """</strong>
    </p>
    <p>
    <a href="/?green_led=on"><button class="button">GREEN ON</button></a>
    </p>
    <p>
    <a href="/?green_led=off"><button class="button button2">GREEN OFF</button></a>
    </p>
    <p>
    SWITCH1 Current State: <strong>""" + switch1_state + """</strong>
    </p>
    <p>
    SWITCH2 Current State: <strong>""" + switch2_state + """</strong>
    </p>
    </body>
    </html>"""
    return html_webpage

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    red_led_on = request.find('/?red_led=on')
    red_led_off = request.find('/?red_led=off')
    green_led_on = request.find('/?green_led=on')
    green_led_off = request.find('/?green_led=off')
    if red_led_on == 6:
        print('RED ON')
        red_led.value(1)
    if red_led_off == 6:
        print('RED OFF')
        red_led.value(0)
    if green_led_on == 6:
        print('GREEN ON')
        green_led.value(1)
    if green_led_off == 6:
        print('GREEN OFF')
        green_led.value(0)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
