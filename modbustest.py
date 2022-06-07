import modbusTCP

c = modbusTCP.MB_Client('10.0.1.221', 502)
# for i in range(10):
a = c.readHReg(26, 10)
version = ""
for i in a:
    version = version + chr(i)
print(version)
