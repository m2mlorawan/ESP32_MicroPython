This repository is where we keep MicroPython Program for ESP32.
It is expected to be used with Maxiiot DL7612-AS923-TH to bult a lorawan Class C node.
Downlink in class C is suported by the modules. The example shows how to use thread
to service a realtime donwlink payload. If the payload is equal to definded text, led will be on. 
The example also use cayanee.LPP format for payload.
