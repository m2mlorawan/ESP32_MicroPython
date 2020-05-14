#ESP32 AT

import CCS811, bme280, ssd1306, time, ubinascii, machine
from machine import UART, Pin, I2C
from struct import unpack
from cayennelpp import CayenneLPP
temp = 0
pa = 0
hum = 0
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))

bme = bme280.BME280(i2c=i2c)
uart = UART(2, 115200,timeout=2000)

uart.write('AT+NRB\r\n')
print(uart.read()) 
time.sleep(20.0)
uart.write('AT\r\n')
print(uart.read()) 

cnt = 1
while True:
    print("********Packet No #{}".format( cnt ) )
    temp,pa,hum = bme.values 
    print("********BME280 values:")
    #print(bme.values)
    temp,pa,hum = bme.values
    print('temp:',temp,' Hum:',hum ,'PA:', pa)
    c = CayenneLPP()
    c.addTemperature(1, float(temp)) # Add temperature read to channel 1 
    c.addRelativeHumidity(2, float(hum)) # Add relative humidity read to channel 2
    c.addBarometricPressure(3, float(pa)) 
 
    d = (ubinascii.hexlify(c.getBuffer()))

    print('---------Start Send Status------------')
    print("AT+NMGS={0},{1}\r\n".format(int(len(d)/2),(d.decode('utf-8'))))
    uart.write("AT+NMGS={0},{1}\r\n".format(int(len(d)/2),(d.decode('utf-8'))))
    print(uart.read())
    print('---------End Send Status------------')
    cnt = cnt + 1
    time.sleep(5.0)