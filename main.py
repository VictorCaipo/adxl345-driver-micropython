from machine import Pin, I2C
from adxl345 import ADXL345
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

#debugg
    #scan devuelve una lista vacia el problema es electrico
print("Escaneando bus I2C...")
dispositivos = i2c.scan()
print(f"Dispositivos encontrados: {[hex(d) for d in dispositivos]}")
#debugg

#It is necessary to always state the constructure
sensor = ADXL345(i2c)
sensor.set_data_rate(100)
sensor.resolution(4)
print("Confguracion exitosa")
time.sleep(2)

while True:
    x, y, z = sensor.data_lecture()
    print(f"Eje X: {x:6d} | Eje Y: {y:6d} | Eje Z: {z:6d}")
    time.sleep(1)
