"""Example usage basic driver CCS811.py"""

from machine import Pin, I2C  
import time
import CCS811
import machine
import Assd1306
import bme280


def main():
    i2c = I2C(scl=Pin(22), sda=Pin(21)) #ESP32 Dev Board /myown
    # CCS811 sensor 
    s = CCS811.CCS811(i2c)
    bme = bme280.BME280(i2c=i2c,address=118)
    d = Assd1306.SSD1306_I2C(128,64,i2c,0x3c)
    time.sleep(1)

    while True:
       print("**************")
       print("BME280 values:")
       print("**************")
       #print(bme.values)
       temp,pa,hum = bme.values
       print('temp:',temp,' Hum:',hum ,'PA:', pa)
       d.fill(0)
       d.text("Temp. "+temp, 0, 0)
       d.text("Hum. "+hum, 0, 10)
       d.text("PA "+pa, 0, 20)
       d.show()
       
       if s.data_ready():
            print(" ")
            print("**************")
            print("CSS811 values:")
            print("**************")
            print('eCO2: %d ppm, TVOC: %d ppb' % (s.eCO2, s.tVOC))
            print(" ")
            #d.fill(0)
            d.text('eCO2 ppm',0,30)
            d.text(str(s.eCO2),70,30)
            d.text('TVOC ppb',0,40)
            d.text(str(s.tVOC),70,40)
            d.show()
            time.sleep(3)

main()

