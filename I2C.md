# I2C library

- I have written adxl345 based on I2C library supported by MicroPython. I am summarizing all functions to be used on the adxl345 driver.

> https://docs.micropython.org/en/latest/library/machine.I2C.html


## 1. I2C(id, *, scl, data, freq=400000, timeout=50000)[constructor]
- It constructs and returns a new I2C object using the following parameters:
    - id identifies a particular I2C peripheral, some microcontrollers have more than one, be careful /ˈker.fəl/.
    - scl should be a pin object used for SCL
    - sda should be a pin object used for SDA
    - freq should be an integer which sets the maximum frequency for SCL.
    - timeout is the maximum time in microseconds to allow for I2C transactions.

## 2. I2C.scan()[method]
- Scan all I2C addresses (of peripherals) between 0x08 and 0x77 inclusive and return a list of those that respond. So, it is easy to know what peripheral are we getting connected.

## 3. I2C.readfrom_mem(addr, memaddr, nbytes, *, addrsize=8)[method]
- Read nbytes from the peripheral specified by addr starting from the memory address specified by memaddr.  The argument addrsize specifies the address size in bits.

## 4. I2C.writeto_mem(addr. memaddr, buf, *, addrsize=8)[method]
- Write buf to the peripheral specified by addr starting from the memory address specified by memaddr.