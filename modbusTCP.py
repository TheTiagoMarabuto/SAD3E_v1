import random

from pyModbusTCP.client import ModbusClient
from pyModbusTCP.server import ModbusServer, DataBank

import random
from time import sleep

ADDR = 1000


class MB_Client:
    def __init__(self, server_ip, port):
        self._client = ModbusClient(host=server_ip, port=port)

    def startConnection(self):
        self._client.open()

    def endConnection(self):
        self._client.close()

    def sleep(self, sleep_time):
        self.sleep(sleep_time)

    def readCoil(self, address):
        return self._client.read_coils(address)[0]

    def readHReg(self, address, ntimes):
        return self._client.read_holding_registers(address, ntimes)

    def writeCoil(self, address, data):
        self._client.write_single_coil(address, data)

    def writeHReg(self, address, data):
        self._client.write_single_register(address, data)


def device_states(MBClient, available_array):
    d_states = []
    for loop, device_n, availability in available_array:
        if loop == 1:
            d_states.append([loop, device_n, MBClient.readHReg(10242 + 10 * (device_n - 1), 1)])
        if loop == 2:
            d_states.append([loop, device_n, MBClient.readHReg(15322 + 10 * (device_n - 1), 1)])
        if loop == 3:
            d_states.append([loop, device_n, MBClient.readHReg(20402 + 10 * (device_n - 1), 1)])
        if loop == 4:
            d_states.append([loop, device_n, MBClient.readHReg(25482 + 10 * (device_n - 1), 1)])
    d_states.sort()
    return d_states


def available_devices(MBClient):
    print("available_devices(): Getting available devices...\r")
    loop_availability = available_loops(MBClient)
    available_array = []
    # loop through 254 possibly available devices
    for d in range(1, 4):
        # First loop
        if loop_availability[0] and MBClient.readCoil(10244 + 10 * (d - 1)):
            available_array.append((1, d, True))
        # Second loop
        if loop_availability[1] and MBClient.readCoil(15324 + 10 * (d - 1)):
            available_array.append((2, d, True))
        # Third loop
        if loop_availability[2] and MBClient.readCoil(20404 + 10 * (d - 1)):
            available_array.append((3, d, True))
        # Forth loop
        if loop_availability[3] and MBClient.readCoil(25484 + 10 * (d - 1)):
            available_array.append((4, d, True))
    available_array.sort()
    print("available_devices(): Finished \r")
    return available_array


def available_loops(MBClient):
    loops = []

    # check available loops
    loops.insert(0, MBClient.readCoil(910))  # loop 1 availability coil
    loops.insert(1, MBClient.readCoil(942))  # loop 2 availability coil
    loops.insert(2, MBClient.readCoil(974))  # loop 3 availability coil
    loops.insert(3, MBClient.readCoil(1006))  # loop 4 availability coil

    return loops
