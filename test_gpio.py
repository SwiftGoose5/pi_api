import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

print("Blinking GPIO 17...")
for i in range(5):
    GPIO.output(17, GPIO.HIGH)
    print("HIGH")
    time.sleep(0.5)
    GPIO.output(17, GPIO.LOW)
    print("LOW")
    time.sleep(0.5)

GPIO.cleanup()
print("Done")
