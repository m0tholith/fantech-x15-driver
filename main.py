from dataclasses import dataclass

import usb.core
import usb.util

PACKET_SIZE = 8


class deviceInfo:
    vendor = 0x18F8
    product = 0x0FC0
    bRequestType = 0x21
    bRequest = 0x09
    wIndex = 0x0307


@dataclass
class PacketPack:
    size: int
    packets: list[list[int]]


def get_packets_to_send() -> list[PacketPack]:
    packetsFile = open(r"./packets", "r")
    packetsStr: list[str] = packetsFile.readlines()

    packetPackCount: int = 1 + packetsStr.count("\n")

    packets: list[list[int]] = []
    for i in range(len(packetsStr)):
        packetsStr[i] = (packetsStr[i])[0:-1]
        if len(packetsStr[i]) <= 1:
            continue
        hexarr: list[int] = [int(j, 16) for j in packetsStr[i].split()]
        packets.append(hexarr)

    packetPackSize = len(packets) // packetPackCount

    packetsFile.close()

    return [
        PacketPack(
            packetPackCount,
            packets[0:packetPackSize],
        ),
        PacketPack(
            packetPackCount,
            packets[packetPackSize : packetPackSize * 2],
        ),
        PacketPack(
            packetPackCount,
            packets[packetPackSize * 2 :],
        ),
    ]

    # print("packetPackSize", packetPackSize)
    # print("packetPackCount", packetPackCount)
    # print("len(packetsStr)", len(packetsStr))
    # print("len(packets)", len(packets))
    #
    # for packetIdx in range(packetPackCount * packetSize):
    #     print("%0.8d:" % packetIdx, end="	")
    #     print(
    #         "".join(
    #             ["%0.2X " % i for i in packets[packetIdx + 0 * packetPackSize]]
    #         ),
    #         end="	",
    #     )
    #     print(
    #         "".join(
    #             ["%0.2X " % i for i in packets[packetIdx + 1 * packetPackSize]]
    #         ),
    #         end="	",
    #     )
    #     print(
    #         "".join(
    #             [
    #                 "%0.2X "
    #                 % abs(
    #                     packets[packetIdx + 0 * packetPackSize][i]
    #                     - packets[packetIdx + 1 * packetPackSize][i]
    #                 )
    #                 for i in range(packetSize)
    #             ]
    #         ),
    #         end="	",
    #     )
    #     print()


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

# write the data
packetPacks = get_packets_to_send()
for i in packetPacks[1].packets:
    dev.ctrl_transfer(
        deviceInfo.bRequestType,
        deviceInfo.bRequest,
        deviceInfo.wIndex,
        intf.bInterfaceNumber,
        i,
    )

usb.util.release_interface(dev, intf.bInterfaceNumber)
dev.attach_kernel_driver(intf.bInterfaceNumber)
