# Reference: https://pinout.xyz/ 
#            https://gpiozero.readthedocs.io/en/latest/index.html 

from gpiozero import LED
from time import sleep

led = LED(17)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)