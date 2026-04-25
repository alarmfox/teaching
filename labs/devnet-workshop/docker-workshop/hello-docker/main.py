import platform
import sys

print("Hello, you are executing me from", platform.machine(), "processor")
print("Platform information:", platform.platform())
print("OS:", platform.system())
print("Python:", sys.version)
name = input("Give me your name: \n")

print("Hello,", name)
