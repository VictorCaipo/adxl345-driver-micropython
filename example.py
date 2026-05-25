import time
from machine import Pin, I2C
from adxl345 import ADXL345

#   Setting up I2C object
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

#   Initializing ADXL345 constructor
sensor = ADXL345(i2c)

#   Configuring resolution and data rate
sensor.resolution(4) # (Options: 2, 4, 8, 16)
sensor.set_data_rate(100) # (Options: 50, 100, 200, 400)

#   Getting acceleration
while True:
    x, y, z = sensor.get_acceleration()
    print(f"X:{x:+.3f}g  |  Y:{y:+.3f}g  |  Z:{z:+.3f}g")
    time.sleep(2)