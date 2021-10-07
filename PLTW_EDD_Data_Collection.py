import Netster
import time
import datetime
import sys
import threading
import processor
import multiprocessing

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
        elif (userInput == "pr"):
            multiprocessing.Process(target=processor.main).start()
            print("Processed log")
        else:
            print("Unknown command!")
        

def log(msg):
    f = open("log.txt", "a")
    dt = datetime.datetime.now()
    f.write(str(dt.month) + "." + str(dt.day) + "." + str(dt.year) + "_" + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second) + " - " + msg + "\n")
    f.close()

def main(args):
    del args[0]
    n._pingAddresses.extend(args)
    while ((datetime.datetime.now().second % 10) != 0):
        pass
    while (run):
        dt = datetime.datetime.now()
        if ((dt.hour == 3) and (dt.minute < 1)):
            log(str(n.speedtest()))
        else:
            past = time.time()
            log(str(n.ping()))
            time.sleep(10 - (time.time() - past) - 0.008)

if (__name__ == "__main__"):
    threading.Thread(target=main, args=(sys.argv,)).start()
    console()
    quit()