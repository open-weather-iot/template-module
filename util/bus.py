import machine
from machine import Pin

SPI_SELECT = 0
SPI_DESELECT = 1

class SPI:
    BUS_BAUDRATE = 115200

    def __init__(self, *, port):
        # values not yet fixed. those will be derived from 'port'
        spi_id   = 1
        sck_pin  = 10
        mosi_pin = 11
        miso_pin = 12
        cs_pin   = 13

        self.CS = Pin(cs_pin, mode=Pin.OUT)
        self.CS.value(SPI_DESELECT)

        self.spi = machine.SPI(
            spi_id, 
            baudrate=self.BUS_BAUDRATE, polarity=0, phase=1, firstbit=machine.SPI.MSB, 
            sck=Pin(sck_pin, Pin.OUT),
            mosi=Pin(mosi_pin, Pin.OUT),
            miso=Pin(miso_pin, Pin.OUT),
        )

    def __enter__(self):
        self.select()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.deselect()

    def select(self):
        self.CS.value(SPI_SELECT)

    def deselect(self):
        self.CS.value(SPI_DESELECT)

    def read(self, nbytes, *, auto_select=False):
        if auto_select: self.select()
        value = self.spi.read(nbytes)
        if auto_select: self.deselect()
        return value

    def write(self, buf, *, auto_select=False):
        if auto_select: self.select()
        self.spi.write(buf)
        if auto_select: self.deselect()

# TODO
class Serial:
    def __init__(self, *, port):
        pass


# TODO
class I2C:
    def __init__(self, *, bus, addr):
        pass
