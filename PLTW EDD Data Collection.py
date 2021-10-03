import Netster
import time
import datetime
import os
import threading

run = True
n = Netster.Netster()

def console():
    global run
    while True:
        userInput = input(">:")
        if (userInput == "quit"):
            run = False
            print("Bye!")
            break
        elif (userInput[0:4] == "add "):
            n.add_ping_address(userInput[4:])
            print("Added IP/Hostname.")
        elif (userInput[0:3] == "rm "):
            n.remove_ping_address(userInput[3:])
            print("Removed IP/Hostname.")
        else:
            print("Unknown command!")
        

def log(msg):
    f = open("log.txt", "a")
    f.write(datetime.datetime.now().ctime() + " - " + msg + "\n")
    f.close()

def main():
    while ((datetime.datetime.now().second % 10) != 0):
        pass
    while (run):
        dt = datetime.datetime.now()
        if ((dt.hour == 3) and (dt.minute < 1)):
            log(str(n.speedtest()))
        else:
            past = time.time()
            log(str(n.ping()))
            time.sleep(10 - (time.time() - past))

if (__name__ == "__main__"):
    threading.Thread(target=main).start()
    console()
    quit()