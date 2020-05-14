import si7021
import machine
from machine import Pin, I2C  
i2c = I2C(scl=Pin(22), sda=Pin(21)) #ESP32 Dev Board /myown
temp_sensor = si7021.Si7021(i2c)
print('Temp :{value}'.format(value=temp_sensor.temperature))
print('Humid:{value}'.format(value=temp_sensor.relative_humidity))
#print (temp_sensor.temperature)
#print (temp_sensor.relative_humidity)