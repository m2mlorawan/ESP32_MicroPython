This repository is where we keep MicroPython Program for ESP32.
It is expected to be used with Maxiiot DL7612-AS923-TH to build a lorawan Class C node.

12_ESP32CCS8128OLED.py
This is a full an complete class C example. Downlink in class C is suported by the modules. The example use thread
to service a realtime donwlink payload. If the Downlink payload is equal to definded text, led will be on. 
The example also use cayaneeLPP format for payload. The node will try to join OTAA until success.

A CCS8128 sensor is composed of CCS811, SI7021, BMP280. Sensor data were read and displayed on SSD1308. We rename SSD1308 to ASSD1308 to avoid conflict with SSD3018 in internal lib.  A blue LED with flash one time when the packet is sent out.  
