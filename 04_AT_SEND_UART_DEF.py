#ESP32 UNO03
#rx=16, tx=17

from machine import UART
import time
from time import sleep
uart = UART(2, 115200,timeout=20)

def sendATcommand(ATcommand):
    print("{0}\r\n".format(ATcommand))
    uart.write("{0}\r\n".format(ATcommand))
    print(uart.read().decode('utf-8'))
    sleep(4)

#sendATcommand ("AT+NCONFIG")
sendATcommand ('AT+NMGR')
#sendATcommand ('AT+NCONFIG')
#sendATcommand ('AT+CGATT')
#sendATcommand ('AT+NCMGS=5,HELLO')

#sendATcommand ("AT+APPKEY")
##sendATcommand ("AT+RESTORE")
#sendATcommand ('AT+INFO')
#sendATcommand ('AT+NCONFIG')
#sendATcommand ('AT+DEBUG=1')

#sendATcommand ('AT+CLASS=C')
#sendATcommand ('AT+NNMI=0')
#sendATcommand ('AT+SAVE')
#sendATcommand ('AT+NRB')
#sendATcommand ('AT+NCONFIG')
#sendATcommand ("AT+DEVEUI")
#sendATcommand ("AT+DEBUG=1")
#sendATcommand ("AT+ACTIVATE=0")
#sendATcommand ("AT+AT+SAVE")
#sendATcommand ("AT+AT+NCONFIG")

