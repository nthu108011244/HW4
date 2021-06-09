import time
import serial

def get_command():
    command = input()
    if command == "quit": 
        return 0
    else:
        print(command[:])
        return 1
    

while get(): 
    j = 0