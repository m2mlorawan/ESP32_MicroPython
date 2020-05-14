__author__ = __maintainer__ = "Helder Moreira"
__license__ = "MIT"
__version__ = "1.0.0"

# TYPE: [IPSO OBJ, SIZE(S)]
TYPE = {
    'LPP_DIGITAL_INPUT': [3200, 1],
    'LPP_DIGITAL_OUTPUT': [3201, 1],
    'LPP_ANALOG_INPUT': [3202, 2],
    'LPP_ANALOG_OUTPUT': [3203, 2],
    'LPP_LUMINOSITY': [3301, 2],
    'LPP_PRESENCE': [3302, 1],
    'LPP_TEMPERATURE': [3303, 2],
    'LPP_RELATIVE_HUMIDITY': [3304, 1],
    'LPP_ACCELEROMETER': [3313, (2, 2, 2)],
    'LPP_BAROMETRIC_PRESSURE': [3315, 2],
    'LPP_GYROMETER': [3334, (2, 2, 2)],
    'LPP_GPS': [3336, (3, 3, 3)],
}


def to_bytes(value, size):
    if value > pow(2, 8 * size):
        raise OverflowError('int too big to convert')
    b = bytearray()
    for i in range(size - 1, -1, -1):
        b.append((value >> (i * 8)) & 0x00ff)
    return b


class CayenneLPP(object):
    def __init__(self, maxsize=0):
        self._maxsize = maxsize
        self.reset()

    def _add_to_buffer(self, dtype, channel, *value):
        try:
            data_type, data_size = TYPE[dtype]
            if type(data_size) == int:
                data_size = (data_size,)
            temp_buff = bytearray()
            temp_buff.append(channel)
            temp_buff.append(data_type - 3200)

            for i in range(0, len(data_size)):
                # temp_buff+=int(value[i]).to_bytes(data_size[i],'big')  #NOT FULLY IMPLEMENTED IN MICROPYTHON
                temp_buff += to_bytes(int(value[i]), data_size[i])

            assert self._maxsize == 0 or self.getSize() + len(temp_buff) <= self._maxsize
            self._buffer += temp_buff
            return True
        except:
            return False

    def reset(self):
        self._buffer = bytearray()

    def getSize(self):
        return len(self._buffer)

    def getBuffer(self):
        return self._buffer

    def copy(self, buf):
        self._buffer = buf

    def addDigitalInput(self, channel, value):
        return self._add_to_buffer('LPP_DIGITAL_INPUT',
                                   channel,
                                   value)

    def addDigitalOutput(self, channel, value):
        return self._add_to_buffer('LPP_DIGITAL_OUTPUT',
                                   channel,
                                   value)

    def addAnalogInput(self, channel, value):
        return self._add_to_buffer('LPP_ANALOG_INPUT',
                                   channel,
                                   round(value, 2) * 100)

    def addAnalogOutput(self, channel, value):
        return self._add_to_buffer('LPP_ANALOG_OUTPUT',
                                   channel,
                                   round(value, 2) * 100)

    def addLuminosity(self, channel, value):
        return self._add_to_buffer('LPP_LUMINOSITY',
                                   channel,
                                   value)

    def addPresence(self, channel, value):
        return self._add_to_buffer('LPP_PRESENCE',
                                   channel,
                                   value)

    def addTemperature(self, channel, value):
        return self._add_to_buffer('LPP_TEMPERATURE',
                                   channel,
                                   round(value, 1) * 10)

    def addRelativeHumidity(self, channel, value):
        return self._add_to_buffer('LPP_RELATIVE_HUMIDITY',
                                   channel,
                                   round(value * 2))

    def addBarometricPressure(self, channel, value):
        return self._add_to_buffer('LPP_BAROMETRIC_PRESSURE',
                                   channel,
                                   round(value, 1) * 0.1)

    def addAccelerometer(self, channel, x, y, z):
        return self._add_to_buffer('LPP_ACCELEROMETER',
                                   channel,
                                   round(x, 3) * 1000,
                                   round(y, 3) * 1000,
                                   round(z, 3) * 1000)

    def addGyrometer(self, channel, x, y, z):
        return self._add_to_buffer('LPP_BAROMETRIC_PRESSURE',
                                   channel,
                                   round(x, 2) * 100,
                                   round(y, 2) * 100,
                                   round(z, 2) * 100)

    def addGPS(self, channel, latitude, longitude, meters):
        return self._add_to_buffer('LPP_GPS',
                                   channel,
                                   round(latitude, 4) * 10000,
                                   round(longitude, 4) * 10000,
                                   round(meters, 2) * 100)

