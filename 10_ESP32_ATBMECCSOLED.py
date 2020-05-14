# By Somsak Lima and Itti  Srisumalai
#ESP32 UNO03
#rx=16, tx=17
import ure
import CCS811, bme280, Assd1306, time, ubinascii, machine
import SSD1306
from machine import UART, Pin, I2C
from struct import unpack
from cayennelpp import CayenneLPP
from time import sleep
led = Pin(2, Pin.OUT)
temp = 0
pa = 0
hum = 0

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21)) #ESP32 Dev Board /myown

#s = CCS811.CCS811(i2c=i2c)
bme = bme280.BME280(i2c=i2c)
d = Assd1306.SSD1306_I2C(128,64,i2c,0x3c)
uart = UART(2, 115200,timeout=2000)

print(uart.read()) 
uart.write('AT+NRB\r\n')
print(uart.read()) 
time.sleep(20.0)
uart.write('AT\r\n')
print(uart.read()) 
uart.write('AT+NCONFIG\r\n')
print(uart.read())


cnt = 1
while True:
    print( "Packet No #{}".format( cnt ) )
    temp,pa,hum = bme.values 
    print("**************")
    print("BME280 values:")
    print("**************")
    #print(bme.values)
    temp,pa,hum = bme.values
    print('temp:',temp,' Hum:',hum ,'PA:', pa)
    d.fill(0)
    d.text("#",95,50)
    d.text(str(cnt),102,50)
    d.text("Temp. "+temp, 0, 0)
    d.text("Hum. "+hum, 0, 10)
    d.text("PA "+pa, 0, 20)
    d.show()
    #time.sleep(3)
    s = CCS811.CCS811(i2c=i2c) #Need to fixed error
    time.sleep(10)
    if s.data_ready():
     
        print(" ")
        print("**************")
        print("CSS811 values:")
        print("**************")
        print('eCO2: %d ppm, TVOC: %d ppb' % (s.eCO2, s.tVOC))
        print(" ")
        #time.sleep(1)
        #d.fill(0)
        d.text('eCO2 ppm',0,30)
        d.text(str(s.eCO2),70,30)
        d.text('TVOC ppb',0,40)
        d.text(str(s.tVOC),70,40)
        d.show()
        time.sleep(3)

        
    c = CayenneLPP()
    c.addTemperature(1, float(temp)) # Add temperature read to channel 1 
    c.addRelativeHumidity(2, float(hum)) # Add relative humidity read to channel 2
    c.addBarometricPressure(3, float(pa)) 
    c.addLuminosity(4,  s.eCO2);
    c.addLuminosity(5,  s.tVOC);
  
    #cno=len(ubinascii.hexlify(c.getBuffer()))    
    b = (ubinascii.hexlify(c.getBuffer()))
    #cno=len(b)  
    print('---------Send Status------------')
    print("AT+NMGS={0},{1}\r\n".format(int(len(b)/2),(b.decode('utf-8'))))
    uart.write("AT+NMGS={0},{1}\r\n".format(int(len(b)/2),(b.decode('utf-8'))))
    p = ure.search('FRMPayload:(.+?) \r\n', uart.read().decode('utf-8'))
    
    try:
        print (p.group(1))
        pgroup=(p.group(1))
    except AttributeError:
        pgroup=""
        print ('Not found Downlink Packet')

    if pgroup==" aa bb cc":
        print("Command1 Detected: On LED  =============>")
        led.value(not led.value())
        sleep(0.5)
    else:
        print("No Known Command Detect")
    
    print("++++++++++")
    print('---------Send Status------------')
    #if cnt >= 1000000:
    #    break
    cnt = cnt + 1
    time.sleep(5.0)