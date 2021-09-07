import serial
import crcmod
import time

SET_MODE_DISABLE = b'\xAA\x55\x50\x03\x02\x00'
SET_MODE_1 = b'\xAA\x55\x50\x03\x02\x01'
CHECK_STATUS = b'\xAA\x55\x51\x02\x02'

# Establish Serial Communication
# put the correct device handle here

class Oximeter:
    def __init__(self, port='/dev/ttyUSB0', baudrate=38400) -> None:
        '''
            Init
        '''
        # setup and connect
        self.port = port
        self.baudrate = baudrate
        self.serial = None

    def connect(self):
        while not self.serial.is_open:
            try:
                self.serial = serial.Serial(self.port, self.baudrate)
            except serial.SerialException:
                print("Serial Communication Error... Retrying...")

    def setMode(self, mode):
        '''
            set mode
        '''
        if mode == 0:
            data = SET_MODE_DISABLE  # set to wave 1 mode.
        elif mode == 1:
            data = SET_MODE_1  # set to wave 1 mode.
        elif mode == 2:
            data = CHECK_STATUS  # check status.
        crc_func = crcmod.predefined.mkCrcFun('crc-8-maxim')
        pack = data + bytes([crc_func(data)])

        # use crc8 maxim, according to the doc
        self.ser.write(pack)
        head = self.ser.read(4)
        body = self.ser.read(head[3])
        receive = head + body
        
        # check return value to guarantee the correct mode is set
        while pack != write:
            self.ser.write(pack)
            head = self.ser.read(4)
            body = self.ser.read(head[3])
            receive = head + body
            for b in receive:
                print(hex(b), end=" ")
            print("")
        print("Setting Mode to {}".format(mode)

    def run(self:
        pass

    def monitor(self):
        while True:
            head = self.ser.read(4)
            body = self.ser.read(head[3])
            receive = head + body
            for b in receive:
                print(hex(b), end=" ")
            print("")
            print(self.ser.in_waiting)


