# Copyright 2020 Cas Hoefman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#Basic Setup
import machine
device_id = ('{:02x}{:02x}{:02x}{:02x}'.format(machine.unique_id()[0], machine.unique_id()[1], machine.unique_id()[2], machine.unique_id()[3]))

## start display
import machine
pin16 = machine.Pin(16, machine.Pin.OUT)
pin16.value(1)
import machine, ssd1306
i2c = machine.I2C(scl=machine.Pin(15), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text('MicroPython on', 0, 0)
oled.text('Heltec      32', 0, 10)
oled.text('ID: ' + device_id, 0, 20)
oled.text('by Cas Hoefman', 0, 30)    
oled.show()

# Import some setting from config file & Set the Led Pin
import config
from machine import RTC, Pin
import ntptime 

led_pin = machine.Pin(config.device_config['led_pin'], Pin.OUT) #built-in LED pin
led_pin.value(0)

#Get Wifi Set Up
import network
import time
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(config.wifi_config['ssid'], config.wifi_config['password'])
    while not wlan.isconnected():
        pass
print('network config:', wlan.ifconfig())
oled.text('       Wifi', 0, 10)
oled.show()
led_pin.value(1)

# Now that we are connected set the time
import ntptime
import utime
ntptime.settime()
tm = utime.localtime()
tm = tm[0:3] + (0,) + tm[3:6] + (0,)
machine.RTC().datetime(tm)
timestamp = '{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.000Z'.format(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])
print(timestamp)
timenow = '{:02d}:{:02d}:{:02d}'.format(tm[3], tm[4], tm[5]) 
oled.text('Time: ' + timenow, 0, 40)    
oled.show()
time.sleep(10)

# I2C Interface, genuine Micropython
from bme680 import *
from machine import I2C, Pin
bme = BME680_I2C(I2C(-1, Pin(15), Pin(4)))

for _ in range(15):
    
    #BME680 Readings
    temperature = str(round(bme.temperature, 2))
    humidity = str(round(bme.humidity, 2))
    pressure = str(round(bme.pressure, 2))
    mox = str(round(bme.gas/1000, 2))
    
    #Set the Time
    tm = utime.localtime()
    timestamp = '{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.000Z'.format(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])  
    timenow = '{:02d}:{:02d}:{:02d}'.format(tm[3], tm[4], tm[5])  
    datenow = '{:02d}-{:02d}-{:04d}'.format(tm[1], tm[2], tm[0])
    
    # Print some stuff if you want to see it in your output here or you can update the display here too.
    print('Temp:', temperature)
    print('Humidity:', humidity)
    print('Pressure:', pressure)
    print('MOX:', mox)
    print(timestamp)
    print('-------')
  
    oled.fill(0)
    oled.text('Temp: ' + temperature, 0, 0)
    oled.text('Humidity: ' + humidity, 0, 10)
    oled.text('Pressure: ' + pressure, 0, 20)
    oled.text('MOX: ' + mox, 0, 30)
    oled.text('GMT: ' + timenow, 0, 40)    
    oled.text('Date: ' + datenow, 0, 50)
    oled.show()

    led_pin.value(0)
    time.sleep(5)
    led_pin.value(1) 
    time.sleep(5)
