
class ADXL345:
# 1. Register map (connection to the sensor)
    #atributes    

    _I2C_ADDR           = 0x53 #bus i2c address 

    #registers    
    _REG_DEVID          = 0x00  #device ID adress
    
    _REG_BW_RATE        = 0x2C  #data reate and power mode control
    _REG_POWER_CTL      = 0x2D  #power saving features control
    
    _REG_DATA_FORMAT    = 0x31  #data format control (sensibility)

    _REG_DATAX0         = 0x32  #where sensor save data
    _REG_DATAX1         = 0x33
    _REG_DATAY0         = 0x34
    _REG_DATAY1         = 0x35
    _REG_DATAZ0         = 0x36
    _REG_DATAZ1         = 0x37

    #values
    _ID_EXPECTED        = 0xE5  #expected value  from _REG_DEVID 
    _ENABLE_MEASURE     = 0x08  #mesure bit is on from_REG_POWER_CTLS

    #methods
    def __init__(self, i2c):
        self.i2c = i2c
            
        dev_id = self._read_register(self._REG_DEVID)
        if dev_id != self._ID_EXPECTED:
            print(f"ADXL345 no encontrado. ID actual: {hex(dev_id)}, ID esperado: {hex(self._ID_EXPECTED)}")
        
        print("ADXL345 detected successfully")
            
        # Configurar el sensor para que empiece a medir
        self._write_register(self._REG_POWER_CTL, self._ENABLE_MEASURE)

    def _read_register(self, reg):
        result = self.i2c.readfrom_mem(self._I2C_ADDR, reg, 1)
        #return a list that contains requested bytes
        #self._I2C_ADDR es la direccion fisica del esp32 en el bus I2C
        #reg es la direccion del registro que queremos leer
        #1 es la cantidad de bytes
        return result[0]

    def _write_register(self, reg, value):
        self.i2c.writeto_mem(self._I2C_ADDR, reg, bytes([value]))

#2. Hardware Abstraction Layer HAL
    def _data_lecture(self):
        data = self.i2c.readfrom_mem(self._I2C_ADDR, self._REG_DATAX0, 6)
        #the sensor divide each axis lecture in two registers, so we have to put them together
        x = (data[1] << 8) | data[0] #16 bits o 2 bytes
        y = (data[3] << 8) | data[2]
        z = (data[5] << 8) | data[4]
        #complemento a 2
        ii = 0b1000000000000000 
        if x & ii: 
            x -= 65536
        if y & ii: 
            y -= 65536
        if z & ii: 
            z -= 65536
            
        return x, y, z
    def set_range(self, g_range):
        """Configura el rango de medición: 2, 4, 8 o 16g."""
        # Mapeo del rango deseado a los bits correspondientes del datasheet
        ranges = {2: 0x00, 4: 0x01, 8: 0x02, 16: 0x03}
        if g_range not in ranges:
            raise ValueError("El rango debe ser 2, 4, 8 o 16")
            
        current_format = self._read_register(self._REG_DATA_FORMAT)

        current_format &= 0xFC
        
        new_format = current_format | ranges[g_range]

        self._write_register(self._REG_DATA_FORMAT, new_format)

    def set_data_rate(self, rate_hz):
    
        rates = {
            100: 0x0A,  # Por defecto al encender
            200: 0x0B,
            400: 0x0C,
            800: 0x0D
        }
        if rate_hz not in rates:
            raise ValueError("Tasas soportadas en este ejemplo: 100, 200, 400 u 800 Hz")
            
        self._write_register(self._REG_BW_RATE, rates[rate_hz])