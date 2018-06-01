import time
import sys
sys.path.insert(0, '../app/')
import DisplayManager
from DisplayManager import DisplayManager


try:
    displayManager = DisplayManager()
    while True:
        print("Test #1 - banana")
        displayManager.displayImage('banana')
        time.sleep(1)
        print("Test #2 - apple")
        displayManager.displayImage('apple')
        time.sleep(1)
        print("Test #3 - raspberry")
        displayManager.displayImage('raspberry')
        time.sleep(1)
        print("Test #4 - orange")
        displayManager.displayImage('orange')
        time.sleep(1)
        print("Test #5 - lemon")
        displayManager.displayImage('lemon')
        time.sleep(1)
        print("Test #6 - none")
        displayManager.displayImage('none')
        time.sleep(1)
except Exception as exception:
    print ( "Error while executing Display Manager tests: (%s)" % exception)