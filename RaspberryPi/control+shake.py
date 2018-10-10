import serial #module for serial port communication
from pynput import keyboard

ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

flag = 0


try:
    while 1:
        if flag == 0:
            user1 = "hello"
            ser.write(user1.encode('utf-8'))
            response = ser.readline()
            print("connecting")
            user2 = "ack"
            if response.decode('utf-8') == "ack":
                ser.write(user2.encode('utf-8'))
                print("connecting ok!")
                flag = 1
                
        if flag == 1:
            user = input() + '\n'
            ser.write(user.encode('utf-8'))
            
except KeyboardInterrupt:
    ser.close()


