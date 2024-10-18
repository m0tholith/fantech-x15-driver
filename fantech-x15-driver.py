#!/usr/bin/env python


from enum import Enum

import toml
import usb.core
import usb.util


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
    "dpiloop": 0x06,
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


class mouse:
    def __init__(self) -> None:
        self.vendor = 0x18F8
        self.product = 0x0FC0
        self.bRequestType = 0x21
        self.bRequest = 0x09
        self.wIndex = 0x0307

        self.defaultMouseMode = 0x02
        self.enabledMouseModes = 0b00111111

        dev = usb.core.find(idVendor=self.vendor, idProduct=self.product)
        if dev is None:
            raise ValueError("Device not found")
        self.dev = dev

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
        dev.set_configuration()
        cfg = dev.get_active_configuration()
        self.intf = cfg[(0, 0)]

        usb.util.claim_interface(dev, self.intf.bInterfaceNumber)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        usb.util.release_interface(self.dev, self.intf.bInterfaceNumber)
        self.dev.attach_kernel_driver(self.intf.bInterfaceNumber)

    def sendPacket(self, packet):
        self.dev.ctrl_transfer(
            self.bRequestType,
            self.bRequest,
            self.wIndex,
            self.intf.bInterfaceNumber,
            packet,
        )

    def sendColorPacket(self, idx, rgb):
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
        self.sendPacket(packet)

    def sendKeybindPacket(self, k: key, b):
        self.sendPacket([0x07, 0x10, k.value, b, 0, 0, 0, 0])

    def sendMouseModePacket(self, modeToChange, dpi):
        self.sendPacket(
            [
                0x07,
                0x09,
                (m.defaultMouseMode + 0x3F) & 0xFF,
                ((dpi << 4) | (modeToChange + 7)) & 0xFF,
                self.enabledMouseModes & 0xFF,
                0,
                0,
                0,
            ]
        )

    def sendLedModePacket(self, mode, time=0):
        self.sendPacket([0x07, 0x13, 0x7F, (mode - time) & 0xFF, 0, 0, 0, 0])

    def sendFireSpeedPacket(self, rate):
        self.sendPacket(
            [0x07, 0x12, 0x00, (rate * 37 // 300) & 0xFF, 0, 0, 0, 0]
        )


parsedConfig = toml.load("./config.toml")

with mouse() as m:
    # keybinds
    m.sendKeybindPacket(key.LMB, keybinds[parsedConfig["keymaps"]["lmb"]])
    m.sendKeybindPacket(
        key.SCROLLBUTTON, keybinds[parsedConfig["keymaps"]["scrollbutton"]]
    )
    m.sendKeybindPacket(key.RMB, keybinds[parsedConfig["keymaps"]["rmb"]])
    m.sendKeybindPacket(
        key.FORWARD, keybinds[parsedConfig["keymaps"]["forward"]]
    )
    m.sendKeybindPacket(
        key.BACKWARD, keybinds[parsedConfig["keymaps"]["backward"]]
    )
    m.sendKeybindPacket(key.PLUS, keybinds[parsedConfig["keymaps"]["plus"]])
    m.sendKeybindPacket(key.MINUS, keybinds[parsedConfig["keymaps"]["minus"]])
    # mouse mode
    m.defaultMouseMode = parsedConfig["misc"]["defaultmode"]
    m.enabledMouseModes = 0
    for i in range(len(parsedConfig["modes"])):
        m.enabledMouseModes |= parsedConfig["modes"][i]["enabled"] << (i + 1)
    for i in range(len(parsedConfig["modes"])):
        m.sendMouseModePacket(
            i - 1, dpiValues[parsedConfig["modes"][i]["dpi"]]
        )
        m.sendColorPacket(i, parsedConfig["modes"][i]["color"])
    # led mode
    m.sendLedModePacket(
        ledModes[parsedConfig["led"]["type"]], parsedConfig["led"]["time"]
    )
    m.sendFireSpeedPacket(parsedConfig["misc"]["fireSpeed"])
