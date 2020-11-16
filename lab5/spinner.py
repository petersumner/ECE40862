from machine import Pin, I2C, Timer
import esp32

class MPU:
    ACC_X = 0x3B
    ACC_Y = 0x3D
    ACC_Z = 0x3F
    TEMP = 0x41
    GYRO_X = 0x43
    GYRO_Y = 0x45
    GYRO_Z = 0x47
    
    def __init__(self, i2c):
        self.i2c = i2c
        self.addr = i2c.scan()[0]
        self.i2c.start()
        self.i2c.writeto(0x68, bytearray([107,0]))
        self.i2c.stop()
        print('Initialized MPU6050')
        
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.pitch_offset = 0
        self.roll_offset = 0
        self.yaw_offset = 0
        self.__init_gyro()
        gyro_timer = Timer(3)
        gyro_timer.init(mode=Timer.PERIODIC, callback=self.__update_gyro, period=100)

    def __init_gyro(self):
        gyro_offsets = self.__read_gyro()
        self.roll_offset = gyro_offsets[0]
        self.pitch_offset = gyro_offsets[1]
        self.yaw_offset = gyro_offsets[2]
    
    def __read_gyro(self):
        self.i2c.start()
        gyro_x = self.i2c.readfrom_mem(self.addr, MPU.GYRO_X, 2)
        gyro_y = self.i2c.readfrom_mem(self.addr, MPU.GYRO_Y, 2)
        gyro_z = self.i2c.readfrom_mem(self.addr, MPU.GYRO_Z, 2)
        self.i2c.stop()
        
        gyro_x = self.__bytes_to_int(gyro_x) / 250 * 0.1
        gyro_y = self.__bytes_to_int(gyro_y) / 250 * 0.1
        gyro_z = self.__bytes_to_int(gyro_z) / 250 * 0.1
        
        return gyro_x, gyro_y, gyro_z
    
    def __update_gyro(self, timer):
        gyro_val = self.__read_gyro()
        self.roll += gyro_val[0] - self.roll_offset
        self.pitch += gyro_val[1] - self.pitch_offset
        self.yaw += gyro_val[2] - self.yaw_offset

    def acceleration(self):
        self.i2c.start()
        acc_x = self.i2c.readfrom_mem(self.addr, MPU.ACC_X, 2)
        acc_y = self.i2c.readfrom_mem(self.addr, MPU.ACC_Y, 2)
        acc_z = self.i2c.readfrom_mem(self.addr, MPU.ACC_X, 2)
        self.i2c.stop()
        
        acc_x = self.__bytes_to_int(acc_x) / 16384 * 9.81
        acc_y = self.__bytes_to_int(acc_y) / 16384 * 9.81
        acc_z = self.__bytes_to_int(acc_z) / 16384 * 9.81
        
        return acc_x, acc_y, acc_z
    
    def temperature(self):
        self.i2c.start()
        temp = self.i2c.readfrom_mem(self.addr, self.TEMP, 2)
        self.i2c.stop()
        
        temp = self.__bytes_to_int(temp)
        return self.__celsius_to_fahrenheit(temp / 340 + 36.53)
    
    def gyro(self):
        return self.pitch, self.roll, self.yaw
    
    @staticmethod
    def __celsius_to_fahrenheit(temp):
        return temp*9 / 5 + 32
    
    @staticmethod
    def __bytes_to_int(data):
        if not data[0] & 0x80:
            return data[0] << 8 | data[1]
        return -(((data[0] ^ 0xFF) << 8) | (data[1] ^ 0xFF) + 1)

led_red = Pin(27, Pin.OUT)
led_green = Pin(15, Pin.OUT)
led_yellow = Pin(14, Pin.OUT)
onboard_led = Pin(13, Pin.OUT)

switch1 = Pin(21, Pin.IN)
switch2 = Pin(32, Pin.IN)

i2c = I2C(sda=Pin(22), scl=Pin(23), freq=400000)
print(i2c.scan())
mpu = MPU(i2c)

print(mpu.acceleration())
print(mpu.temperature())
print(mpu.gyro())

       
def switch1_interrupt(pin):
    onboard_led.value(1)
    
def switch2_interrupt(pin):
    onboard_led.value(0)
    
switch1.irq(trigger=Pin.IRQ_RISING, handler=switch1_interrupt)
switch2.irq(trigger=Pin.IRQ_RISING, handler=switch2_interrupt)