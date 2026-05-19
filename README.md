# ***ADXL345 Sensor***

- We are building up a driver for the adxl345 sensor. It is a three-axis digital accelerometer. You can use both I2C and SPI bus serial communication with adxl345. We are using I2C here. 

- To summarize:
    - ESP32 devkitc v4 (microcontroller)
    - ADXL345 (sensor)
    - I2C (serial_bus_communication)


## ***0. Contents***
    1. Register Map
    2. Hardware Abstraction Layer (HAL)
    3. Deriver Logic/ API Layer (main code)
    4. I2C library

> We are going to build a class for each layer */ˈleɪ.ər/*

## ***1. Register Map***
- A register is type of memory (voltail memory). Directly connected to the hardware.


## ***4. I2C library***
- We are using the oficial code provided by micropython creators:
https://docs.micropython.org/en/latest/library/machine.I2C.html
- Here we summarize all used functions on the adxl345.py code.
- We suppose you know (at least in a general context) how I2C works.


***I2C(id, *, scl, data, freq=400000, timeout=50000)[constructor]***
- Construct and return a new I2C object using the following parameters:
    - id identifies a particular I2C peripheral, some microcontrollers have more than one, be careful /ˈker.fəl/.
    - scl should be a pin object used for SCL
    - sda should be a pin object used for SDA
    - freq should be an integer which sets the maximum frequency for SCL.
    - timeout is the maximum time in microseconds to allow for I2C transactions.

***I2C.scan()[method]***
- Scan all I2C addresses (of peripherals) between 0x08 and 0x77 inclusive and return a list of those that respond. So, it is easy to know what peripheral are we getting connected.

***I2C.readfrom_mem(addr, memaddr, nbytes, *, addrsize=8)***
- Read nbytes from the peripheral specified by addr starting from the memory address specified by memaddr.  The argument addrsize specifies the address size in bits.

***I2C.writeto_mem(addr. memaddr, buf, *, addrsize=8)***
- Write buf to the peripheral specified by addr starting from the memory address specified by memaddr.

