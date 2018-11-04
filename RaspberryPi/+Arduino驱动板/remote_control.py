import serial #module for serial port communication
from pynput import keyboard

ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

flag = 0
#Note: Serial port read/write returns "byte" instead of "str" 
#ser.write("testing serial connection\n".encode('utf-8'))
#ser.write("sending via RPi\n".encode('utf-8'))

def on_press(key):
    try:
        print('alphanumeric key  {0} pressed'.format(key.char))
        user = key.char + '\n'
        ser.write(user.encode('utf-8'))
		
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    print('{0} released'.format(key))
    user = 'x' + '\n'
    ser.write(user.encode('utf-8'))
	
    if key == keyboard.Key.esc:
        return False

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
            with keyboard.Listener(
                on_press = on_press,
                on_release = on_release) as listener:
                listener.join()
            #user = input() + '\n'
            #ser.write(user.encode('utf-8'))
            
except KeyboardInterrupt:
    ser.close()


