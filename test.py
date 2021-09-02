import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as animation
from numpy.core.shape_base import block
import serial
import crcmod
import time


SET_MODE_DISABLE = b'\xAA\x55\x50\x03\x02\x00'

SET_MODE_1 = b'\xAA\x55\x50\x03\x02\x01'

CHECK_STATUS = b'\xAA\x55\x51\x02\x02'

# Establish Serial Communication
# put the correct device handle here
ser = serial.Serial('/dev/ttyUSB1', baudrate=38400)


def Set(mode):
    if mode == 0:
        data = SET_MODE_DISABLE  # set to wave 1 mode.
    elif mode == 1:
        data = SET_MODE_1  # set to wave 1 mode.
    elif mode == 2:
        data = CHECK_STATUS  # check status.
    crc_func = crcmod.predefined.mkCrcFun('crc-8-maxim')
    pack = data + bytes([crc_func(data)])
    # use crc8 maxim, according to the doc
    ser.write(pack)
    head = ser.read(4)
    body = ser.read(head[3])
    receive = head + body

    # check return value to guarantee the correct mode is set
    while head[2] != data[2]:
        body = ser.read(head[3])
        receive = head + body
        for b in receive:
            print(hex(b), end=" ")
        print("")
        ser.write(pack)
        head = ser.read(4)
    body = ser.read(head[3])
    receive = head + body
    for b in receive:
        print(hex(b), end=" ")
    print("")


def Monitor():
    while True:
        head = ser.read(4)
        body = ser.read(head[3])
        receive = head + body
        for b in receive:
            print(hex(b), end=" ")
        print("")


def Plot():
    figure = plt.figure()
    ax = figure.add_subplot(111)
    plt.ylim((-10, 200))
    x = np.linspace(0, 2000, 1000)
    y = np.ones(1000)*64
    line,  = ax.plot(x, y, 'b-')
    i = 0
    figure.canvas.draw()
    plt.show(block=False)
    ax.autoscale_view(True, True, True)

    while True:
        head = ser.read(4)
        body = ser.read(head[3])
        receive = head + body
        for b in receive:
            print(hex(b), end=" ")
        if receive[2] == 82:
            y[i] = receive[5] & 0x7F
            print('y: ', y[i])
        else:
            y[i] = 64

        line.set_ydata(y)
        figure.canvas.draw()
        figure.canvas.flush_events()
        if i == 999:
            i = 0
        else:
            i = i + 1