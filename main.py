import time
from machine import Pin, I2C
from adxl345 import ADXL345

# 1. Initialize I2C object 
#   I2C(bus, SCL pin, SDA pin, freq(optional))
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# 2. Initialize ADXL345 constructure
sensor = ADXL345(i2c)

# 3. Configure resolution and bit rate
sensor.resolution(4)        
# Configure the range (Options: 2, 4, 8, 16)
sensor.set_data_rate(100)   
# Configue data rate (Options: 50, 100, 200, 400)

# 4. Getting acceleration
while True:
    x, y, z = sensor.get_acceleration()
    print(f"X: {x:+.3f} g  |  Y: {y:+.3f} g  |  Z: {z:+.3f} g")
    time.sleep(1)