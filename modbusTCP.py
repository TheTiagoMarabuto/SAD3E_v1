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

    def readHReg(self,address, ntimes):
        return self._client.read_holding_registers(address,ntimes)

    def writeCoil(self, address, data):
        self._client.write_single_coil(address, data)

    def writeHReg(self, address, data):
        self._client.write_single_register(address, data)


class MB_Server:
    def __init__(self, host_ip, port):
        self._server = ModbusServer(host=host_ip, port=port, no_block=True)
        self._db = DataBank

    def run(self):
        try:
            self._server.start()
            print(f"Server Started: {self._server.host} {self._server.port}")

            while True:
                DataBank.set_coils(self._db, 100, [1,0,1])
                #self._db.set_words()
                print(f"Value coil: {DataBank.get_bits(10)} \r\n")
                print(f"Value hreg: {DataBank.get_words(10)} \r\n")
                sleep(1)
        except Exception as e:
            print("Error: ", e.args)
