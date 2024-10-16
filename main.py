from dataclasses import dataclass
from enum import Enum

import usb.core
import usb.util


class deviceInfo:
    vendor = 0x18F8
    product = 0x0FC0
    bRequestType = 0x21
    bRequest = 0x09
    wIndex = 0x0307


class key(Enum):
    LMB = 0x01
    MMB = 0x02
    RMB = 0x03
    FORWARD = 0x04
    BACKWARD = 0x05
    PLUS = 0x08
    MINUS = 0x06


class keybind(Enum):
    LEFTCLICK = 0x01
    MIDDLECLICK = 0x02
    RIGHTCLICK = 0x03
    FORWARD = 0x04
    BACKWARD = 0x05
    DPI_LOOP = 0x06
    SHOW_DESKTOP = 0x07
    DOUBLE_LEFTCLICK = 0x08
    FIRE = 0x09
    OFF = 0x0A
    DPI_PLUS = 0x0B
    DPI_MINUS = 0x0C


class dpiValue(Enum):
    D200 = 0x01
    D400 = 0x02
    D600 = 0x03
    D800 = 0x04
    D1000 = 0x05
    D1200 = 0x06
    D1600 = 0x07
    D2000 = 0x09
    D2400 = 0x0B
    D3200 = 0x0D
    D4000 = 0x0E
    D4800 = 0x0F


dev = usb.core.find(idVendor=deviceInfo.vendor, idProduct=deviceInfo.product)
print(dev)

# was it found?
if dev is None:
    raise ValueError("Device not found")

# fix Resource Busy error
for cfg in dev:
    for intf in cfg:
        if dev.is_kernel_driver_active(intf.bInterfaceNumber):
            try:
                dev.detach_kernel_driver(intf.bInterfaceNumber)
            except usb.core.USBError as e:
                sys.exit(
                    "Could not detatch kernel driver from interface({0}): {1}".format(
                        intf.bInterfaceNumber, str(e)
                    )
                )

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]

# dev.detach_kernel_driver(intf.bInterfaceNumber)
usb.util.claim_interface(dev, intf.bInterfaceNumber)


def sendPacket(packet):
    dev.ctrl_transfer(
        deviceInfo.bRequestType,
        deviceInfo.bRequest,
        deviceInfo.wIndex,
        intf.bInterfaceNumber,
        packet,
    )


def sendColorPacket(idx, r, g, b):
    r = 0xF - r
    g = 0xF - g
    b = 0xF - b
    r, g = g, r
    packet = [
        0x07,
        0x14,
        (((2 * idx) << 4) + r) & 0xFF,
        ((g << 4) + b) & 0xFF,
        0,
        0,
        0,
        0,
    ]
    sendPacket(packet)


def sendKeybindPacket(k: key, b: keybind):
    sendPacket([0x07, 0x10, k.value, b.value, 0, 0, 0, 0])


defaultMouseMode = 0x05
enabledMouseModes = 0b00111111


def sendMouseModePacket(modeToChange, dpi: dpiValue):
    sendPacket(
        [
            0x07,
            0x10,
            (defaultMouseMode + 0x3F) & 0xFF,
            ((dpi.value << 4) | (modeToChange + 7)) & 0xFF,
            0,
            0,
            0,
        ]
    )


# keybinds
sendKeybindPacket(key.LMB, keybind.LEFTCLICK)
sendKeybindPacket(key.MMB, keybind.MIDDLECLICK)
sendKeybindPacket(key.RMB, keybind.RIGHTCLICK)
sendKeybindPacket(key.FORWARD, keybind.FORWARD)
sendKeybindPacket(key.BACKWARD, keybind.BACKWARD)
sendKeybindPacket(key.PLUS, keybind.DPI_PLUS)
sendKeybindPacket(key.MINUS, keybind.DPI_MINUS)
# mouse mode
sendPacket([0x07, 0x09, 0x44, 0x18, 0x3F, 0, 0, 0])
sendPacket([0x07, 0x09, 0x44, 0x39, 0x3F, 0, 0, 0])
sendPacket([0x07, 0x09, 0x44, 0x5A, 0x3F, 0, 0, 0])
sendPacket([0x07, 0x09, 0x44, 0x7B, 0x3F, 0, 0, 0])
sendPacket([0x07, 0x09, 0x44, 0xBC, 0x3F, 0, 0, 0])
sendPacket([0x07, 0x09, 0x44, 0xFD, 0x3F, 0, 0, 0])


# colors


sendColorPacket(0x0, 0x1, 0x1, 0x1)
sendColorPacket(0x1, 0x4, 0x4, 0x5)
sendColorPacket(0x2, 0xC, 0xD, 0xF)
sendColorPacket(0x3, 0x4, 0x7, 0xF)
sendColorPacket(0x4, 0x6, 0xE, 0x6)
sendColorPacket(0x5, 0xF, 0x4, 0x6)
# static led
sendPacket([0x07, 0x13, 0x7F, 0x86, 0, 0, 0, 0])

usb.util.release_interface(dev, intf.bInterfaceNumber)
dev.attach_kernel_driver(intf.bInterfaceNumber)
