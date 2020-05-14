#ESP32 UNO03
#rx=16, tx=17
#from machine import UART

from machine import UART
import time
uart = UART(2, 115200,timeout=20)
uart.write('AT\r\n')
print(uart.read().decode('utf-8')) 
#uart.write('AT+NCONFIG\r\n')
#print(uart.read())
#uart.write('AT+ADDR=2601188C\r\n')
#print(uart.read())
#uart.write('AT+APPSKEY=1506BF244D60B5A46AB1AECA063723AD\r\n')
#print(uart.read())
#uart.write('AT+NWKSKEY=E23ACC607153466B0421B95589B2A3AF\r\n')
#print(uart.read()) 
#uart.write('AT+ACTIVATE=0\r\n')  #ABP Activate
#print(uart.read())
#print(uart.read().decode('utf-8')) 
uart.write('AT+NRB\r\n')
print(uart.read().decode('utf-8')) 
time.sleep(20.0)
uart.write('AT\r\n')
print(uart.read().decode('utf-8')) 
uart.write('AT+NCONFIG\r\n')
print(uart.read().decode('utf-8')) 

cnt = 1
while True:
    print( "Hello! #{}".format( cnt ) )
    #uart.write('AT+NCMGS=5,HELLO\r\n')
    uart.write('AT+NMGS=5,AA112233BB\r\n')
    print(uart.read().decode('utf-8')) 
    uart.write('AT+NMGR\r\n')
    print(uart.read().decode('utf-8')) 
    
    #if cnt >= 100:
    #    break
    cnt = cnt + 1
    time.sleep(5.0)