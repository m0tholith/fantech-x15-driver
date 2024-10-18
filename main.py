from dataclasses import dataclass
from enum import Enum

import toml
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
    SCROLLBUTTON = 0x02
    RMB = 0x03
    FORWARD = 0x04
    BACKWARD = 0x05
    PLUS = 0x08
    MINUS = 0x06


keybinds = {
    "leftclick": 0x01,
    "middleclick": 0x02,
    "rightclick": 0x03,
    "forward": 0x04,
    "backward": 0x05,
    "dpi_loop": 0x06,
    "show_desktop": 0x07,
    "double_leftclick": 0x08,
    "fire": 0x09,
    "off": 0x0A,
    "dpiplus": 0x0B,
    "dpiminus": 0x0C,
}

dpiValues = {
    200: 0x01,
    400: 0x02,
    600: 0x03,
    800: 0x04,
    1000: 0x05,
    1200: 0x06,
    1600: 0x07,
    2000: 0x09,
    2400: 0x0B,
    3200: 0x0D,
    4000: 0x0E,
    4800: 0x0F,
}


ledModes = {
    "off": 0x87,
    "static": 0x86,
    "fixed": 0x86,
    "cyclic": 0x96,
}

dev = usb.core.find(idVendor=deviceInfo.vendor, idProduct=deviceInfo.product)

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


def sendColorPacket(idx, rgb):
    rgb = 0xFFF - rgb
    r = (rgb & 0xF00) >> 8
    g = (rgb & 0x0F0) >> 4
    b = (rgb & 0x00F) >> 0
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


def sendKeybindPacket(k: key, b):
    sendPacket([0x07, 0x10, k.value, b, 0, 0, 0, 0])


defaultMouseMode = 0x02
enabledMouseModes = 0b00111111


def sendMouseModePacket(modeToChange, dpi):
    sendPacket(
        [
            0x07,
            0x09,
            (defaultMouseMode + 0x3F) & 0xFF,
            ((dpi << 4) | (modeToChange + 7)) & 0xFF,
            enabledMouseModes & 0xFF,
            0,
            0,
            0,
        ]
    )


def sendLedModePacket(mode, time=0):
    sendPacket([0x07, 0x13, 0x7F, (mode - time) & 0xFF, 0, 0, 0, 0])


parsedConfig = toml.load("./config.toml")

# keybinds
sendKeybindPacket(key.LMB, keybinds[parsedConfig["keymaps"]["lmb"]])
sendKeybindPacket(
    key.SCROLLBUTTON, keybinds[parsedConfig["keymaps"]["scrollbutton"]]
)
sendKeybindPacket(key.RMB, keybinds[parsedConfig["keymaps"]["rmb"]])
sendKeybindPacket(key.FORWARD, keybinds[parsedConfig["keymaps"]["forward"]])
sendKeybindPacket(key.BACKWARD, keybinds[parsedConfig["keymaps"]["backward"]])
sendKeybindPacket(key.PLUS, keybinds[parsedConfig["keymaps"]["plus"]])
sendKeybindPacket(key.MINUS, keybinds[parsedConfig["keymaps"]["minus"]])
# mouse mode
defaultMouseMode = parsedConfig["misc"]["defaultmode"]
for i in range(len(parsedConfig["modes"])):
    sendMouseModePacket(i - 1, dpiValues[parsedConfig["modes"][i]["dpi"]])
    sendColorPacket(i, parsedConfig["modes"][i]["color"])
# led mode
sendLedModePacket(ledModes[parsedConfig["led"]["type"]], parsedConfig["led"]["time"])

usb.util.release_interface(dev, intf.bInterfaceNumber)
dev.attach_kernel_driver(intf.bInterfaceNumber)
