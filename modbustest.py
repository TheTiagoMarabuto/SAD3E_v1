import modbusTCP
import time
import threading


def device_states(MBClient, available_array):
    d_states = []
    for loop, device_n, availability in available:
        if loop == 1:
            d_states.append([loop, device_n, client.readHReg(10242 + 10 * (device_n - 1), 1)])
        if loop == 2:
            d_states.append([loop, device_n, client.readHReg(15322 + 10 * (device_n - 1), 1)])
        if loop == 3:
            d_states.append([loop, device_n, client.readHReg(20402 + 10 * (device_n - 1), 1)])
        if loop == 4:
            d_states.append([loop, device_n, client.readHReg(25482 + 10 * (device_n - 1), 1)])
    d_states.sort()
    return d_states


def available_devices(MBClient):
    available_array = []
    for d in range(1, 3):
        # First loop
        if loops[0]:
            available_array.append((1, d, client.readCoil(10244 + 10 * (d - 1))))
        # Second loop
        if loops[1]:
            available_array.append((2, d, client.readCoil(15324 + 10 * (d - 1))))
        # Third loop
        if loops[2]:
            available_array.append((3, d, client.readCoil(20404 + 10 * (d - 1))))
        # Forth loop
        if loops[3]:
            available_array.append((4, d, client.readCoil(25484 + 10 * (d - 1))))
    available_array.sort()
    return available_array


client = modbusTCP.MB_Client('10.0.1.221', 502)
# for i in range(10):
start = time.time()
loops = []
# check available loops
loops.insert(0, client.readCoil(910))  # loop 1 availability coil
loops.insert(1, client.readCoil(942))  # loop 2 availability coil
loops.insert(2, client.readCoil(974))  # loop 3 availability coil
loops.insert(3, client.readCoil(1006))  # loop 4 availability coil

print(loops)
print(f"Loop availability DONE in {time.time() - start} seconds")

# check available devices
available = available_devices(client)

while True:
    # check device status : ALARM or NOT
    state = device_states(client, available)
    print(state)
    time.sleep(5)

print(f"took {time.time() - start} to finish")  # version = ""
# for i in a:
#    version = version + chr(i)
# print(version)
