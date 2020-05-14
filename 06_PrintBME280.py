import machine
import bme280
temp = 0
pa = 0
hum = 0
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
bme = bme280.BME280(i2c=i2c)
temp,pa,hum = bme.values 

print(bme.values)
print(temp)
print(pa)
print(hum)




