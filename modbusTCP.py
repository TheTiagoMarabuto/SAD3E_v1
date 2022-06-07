from pyModbusTCP.client import ModbusClient
from pyModbusTCP.server import ModbusServer


class MB_Client():
    def __init__(self, server_ip, port):
        self._client = ModbusClient(host=server_ip, port=port)

    def startConnection(self):
        self._client.open()

    def endConnection(self):
        self._client.close()

    def sleep(self, sleep_time):
        self.sleep(sleep_time)

    def readData(self, address):
        return self._client.read_coils(address)[0]

    def writeData(self, address, data):
        self._client.write_single_coil(address, data)
