class ADXL345:
# 0. Key registers  

    #i2c registers
    _I2C_ADDR           = 0x53 #bus i2c address 

    #sensor registers    
    _REG_DEVID          = 0x00  #device ID adress
    _REG_BW_RATE        = 0x2C  #data rate and power mode control
    _REG_POWER_CTL      = 0x2D  #power saving features control
    _REG_DATA_FORMAT    = 0x31  #data format control (sensibility)
    _REG_DATAX0         = 0x32  #sensor values (accelerometer)
    _REG_DATAX1         = 0x33
    _REG_DATAY0         = 0x34
    _REG_DATAY1         = 0x35
    _REG_DATAZ0         = 0x36
    _REG_DATAZ1         = 0x37

    #values
    _ID_EXPECTED        = 0xE5  #expected value from _REG_DEVID 
    _ENABLE_MEASURE     = 0x08  #mesure bit from_REG_POWER_CTLS
    _RESOLUTION         = 0b00  #resolution 2 by default

# 1. Register map

    def __init__(self, i2c):
        self.i2c = i2c
        dev_id = self._read_register(self._REG_DEVID)
        if dev_id != self._ID_EXPECTED:
            raise RuntimeError(f"Sensor current ID: {hex(dev_id)} | Expected ID: {hex(self._ID_EXPECTED)}")
        self._write_register(self._REG_POWER_CTL, self._ENABLE_MEASURE)
        self._RESOLUTION = 0b00
        self.resolution(2)

    def _read_register(self, reg):
        result = self.i2c.readfrom_mem(self._I2C_ADDR, reg, 1)
        #return a list that contains requested bytes
        #self._I2C_ADDR is the phisical address on the bus I2C
        #reg is the register address we want to read 
        #1 is the quantity of bytes
        return result[0]

    def _write_register(self, reg, value):
        self.i2c.writeto_mem(self._I2C_ADDR, reg, bytes([value]))

# 2. Hardware Abstraction Layer HAL

    def data_lecture(self):
        data = self.i2c.readfrom_mem(self._I2C_ADDR, self._REG_DATAX0, 6)
        #the sensor divide each axis lecture in two registers, so we have to put them together
        x = (data[1] << 8) | data[0] #16 bits or 2 bytes
        y = (data[3] << 8) | data[2]
        z = (data[5] << 8) | data[4]
        ii = 0x8000 #to verify if the number is negative, in bites would be 1000 0000 0000 0000
        if x & ii: #if the number is negative 
            x -= 0x10000 #make two complement to get the real value
        if y & ii: 
            y -= 0x10000
        if z & ii: 
            z -= 0x10000
        return x, y, z
    
    def resolution(self, resl):
        values = {2: 0b00, 4: 0b01, 8: 0b10, 16: 0b11}
        #D1-D0 ranges, check datasheet
        if resl not in values:
            raise ValueError("Choose any of these values: 2, 4, 8, 16")  
        self._RESOLUTION = values[resl]
        current_resolution = self._read_register(self._REG_DATA_FORMAT)
        current_resolution &= 0b11111100#cleaning D1-D0
        new_resolution = current_resolution | self._RESOLUTION
        self._write_register(self._REG_DATA_FORMAT, new_resolution)

    def set_data_rate(self, rate_hz):
        #in the adxl345 datasheet you can find there is plenty of value you could set up
        #we are defining just a couple of them, feel free to modifiy the code
        rate = {400: 0x0C, 200: 0x0B, 100: 0x0A, 50: 0x09}
        if rate_hz not in rate:
            raise ValueError("Choose any of these values: 50, 100, 200, 400")
        self._write_register(self._REG_BW_RATE, rate[rate_hz])

# 3. Application Programming Interface API

    def get_acceleration(self):
        raw_x, raw_y, raw_z = self.data_lecture()
        scale_factor = {0b00:3.9, 0b01:7.8, 0b10:15.6, 0b11:31.2}#mg/LSB
        factor = scale_factor[self._RESOLUTION]/1000 #g/LSB 
        x_g = raw_x * factor
        y_g = raw_y * factor
        z_g = raw_z * factor
        return x_g, y_g, z_g    