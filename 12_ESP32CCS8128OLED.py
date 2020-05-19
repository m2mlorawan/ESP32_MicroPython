# By Somsak Lima and Itti  Srisumalai
# This code is for LoRa module Maxxiot DL7612-AS923-TH
#  
import machine
import ure
import CCS811, bme280, time, ubinascii, machine, si7021
import utime as time
import _thread 
import ssd1306
from machine import UART, Pin, I2C
from struct import unpack
from cayennelpp import CayenneLPP
from time import sleep
from micropython import const


stop = False
#LED_GPIO = const(2)  
#led = machine.Pin( LED_GPIO, mode=machine.Pin.OUT )
led = Pin(2, Pin.OUT)
relay1 = Pin(12, Pin.OUT)
temp = 0
pa = 0
hum = 0
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
bme = bme280.BME280(i2c=i2c)
d = ssd1306.SSD1306_I2C(128,64,i2c,0x3c)
uart = UART(2, 115200,timeout=300)
s = CCS811.CCS811(i2c=i2c)
rstr=""
def sendATcommand(ATcommand):
    print("Command: {0}\r\n".format(ATcommand))
    uart.write("{0}\r\n".format(ATcommand))
    rstr=uart.read().decode('utf-8')
    print(rstr)
    return (rstr)

def led_blink(led):
    global stop
    rstr=""
    while not stop:
        rstr=sendATcommand ('AT+NMGR')
        print("--Downlink Message--: {0}\r\n".format(rstr))

        if "NMGR" in rstr:
            if "040064ff" in rstr:   # BABk/w== 
                print("Command1 Detected: On LED  =============>")
                relay1.value(1)

            elif "040000ff" in rstr:  # BAAA/w==
                print("Command1 Detected: Off LED  =============>")
                relay1.value(0)
            else:
                print("No Known Command Detect")

sendATcommand ('AT')
sendATcommand ('AT+INFO')
sendATcommand ('AT+APPEUI')
sendATcommand ('AT+DEVEUI')
sendATcommand ('AT+APPKEY')
sendATcommand ('AT+NCONFIG')
sendATcommand ('AT+CHSET')
sendATcommand('AT+NRB')

#sendATcommand ('AT+DEBUG=1')
#sendATcommand ('AT+RESTORE')
#sendATcommand ('AT+CLASS=C')
#sendATcommand ('AT+ISMBAND=2')
#sendATcommand('AT+NNMI=0')
#sendATcommand ('AT+SAVE')
#sendATcommand('AT+NMGS=1')
         

while rstr !='+CGATT:1':
        rstr=sendATcommand ('AT+CGATT')
        time.sleep(20.0)
        print('Respond String')
        print(rstr)
        if rstr.startswith('+CGATT:1'):
           print('++++OTAA OK+++++') 
           break
        print('Retry OTAA Continue')

_thread.start_new_thread(led_blink, (led,))

cnt = 1
while True:
    print( "\r\n\r\nPacket No #{}".format( cnt ) )
    temp,pa,hum = bme.values 
    print("*********************")
    print("BME280/BMP280 values:")
    print("*********************")
    temp,pa,hum = bme.values
    print('temp:',temp,' Hum:',hum ,'PA:', pa)
    d.fill(0)
    d.text("#",95,50)
    d.text(str(cnt),102,50)
    d.text("Temp. "+temp, 0, 0)
    d.text("PA "+pa, 0, 20)
    #time.sleep(5)
    
    tsensor = si7021.Si7021(i2c)
    print("**************")
    print("Si7021 values:")
    print("**************")
    print('temp:',tsensor.temperature,' Hum:',tsensor.relative_humidity )

    d.text("Hum. "+str(round(tsensor.relative_humidity,2)), 0, 10)
    d.show()

    
    if s.data_ready():
        print("**************")
        print("CSS811 values:")
        print("**************")
        print('eCO2: %d ppm, TVOC: %d ppb' % (s.eCO2, s.tVOC))

        d.text('eCO2 ppm',0,30)
        d.text(str(s.eCO2),70,30)
        d.text('TVOC ppb',0,40)
        d.text(str(s.tVOC),70,40)
        d.show()
        #time.sleep(3)

    c = CayenneLPP()
    c.addTemperature(1, float(temp)) 
    c.addBarometricPressure(2, float(pa))
    c.addTemperature(3, float(tsensor.temperature)) 
    c.addRelativeHumidity(4, float(tsensor.relative_humidity)) 
    c.addLuminosity(5,  s.eCO2);
    c.addLuminosity(6,  s.tVOC);
    c.addDigitalOutput(7, 1);    
    c.addAnalogOutput(8, 120.0)
  
    b = (ubinascii.hexlify(c.getBuffer()))
    print('************    Sending Data Status   **************')
    led.value(1)
    ATresp=sendATcommand("AT+NMGS={0},{1}".format(int(len(b)/2),(b.decode('utf-8'))))
    print('********Finish Sending & Receiving Data Status******')
    led.value(0)
    cnt = cnt + 1
    time.sleep(10.0)
