import serial

ser = serial.Serial('/dev/cu.usbserial-AL00RIS3', 9600)

while True:
    print(ser.readline())
