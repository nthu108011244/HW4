import time
import serial
import sys,tty,termios
class _Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def get():
    inkey = _Getch()
    while(1):
        k=inkey()
        if k!='':break
    if k=='\x1b':
        k2 = inkey()
        k3 = inkey()
        if k3=='A':
            print ("go forward")
            s.write("/goStraight/run 100 \n".encode())
        if k3=='B':
            print ("go back")
            s.write("/goStraight/run -100 \n".encode())
        if k3=='C':
            print ("turn clockwise")
            s.write("/turn/run 100 -0.3 \n".encode())
        if k3=='D':
            print ("turn counterclockwise")
            s.write("/turn/run 100 0.3 \n".encode())
        time.sleep(1)
        s.write("/stop/run \n".encode())
    elif k=='q':
        print ("quit")
        return 0
    else:
        print ("not an arrow key!")
    return 1

def get_command():
    command = input(">>> Waiting for command: ")
    if command == "over": 
        return 0
    elif command == "park":
        park_mode()
        return 1
    elif command == "line":
        return 1
    elif command == "aptag":
        return 1
    else:
        print(command[:] + " is not keyword")
        return 1

def park_mode():
    print(">>> enter park mode")

    command = input()
    while command != "quit":
        str = command.split(' ')
        d1 = str[0]
        d2 = str[1]
        dirct = str[2]
        if dirct == "west":
            go_back(d1)
            spin_couneterclockwise()
            go_back(int(d2) + 15)
        elif dirct == "east":
            go_back(d1)
            spin_clockwise()
            go_back(int(d2) + 15)
        command = input()

    print(">>> leave park mode")


def go_forward(length):
    print(f"go forward {length}")
    s.write("/goStraight/run 100 \n".encode())
    time.sleep(1) # 1 should be length / velocity
    s.write("/stop/run \n".encode())

def go_back(length):
    print (f"go back {length}")
    s.write("/goStraight/run -100 \n".encode())
    s.write("/LED/write 1 \n".encode())
    time.sleep(1) # 1 should be length / velocity
    s.write("/stop/run \n".encode())
    s.write("/LED/write 0 \n".encode())

def spin_clockwise():
    print ("spin clockwise")
    s.write("/turn/run 100 -1 \n".encode())
    time.sleep(1) # for determined
    s.write("/stop/run \n".encode())

def spin_couneterclockwise():
    print ("spin counterclockwise")
    s.write("/turn/run 100 1 \n".encode())
    time.sleep(1) # for determined
    s.write("/stop/run \n".encode())


# main()
if len(sys.argv) < 1:
    print ("No port input")
s = serial.Serial(sys.argv[1])
while get_command():
    i = 0
'''
while get():
    i = 0
'''