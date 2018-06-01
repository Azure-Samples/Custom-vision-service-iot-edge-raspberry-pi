import sense_hat
from sense_hat import SenseHat
import time
from enum import Enum

class Colors(Enum):
    Green = (0, 255, 0)
    Yellow = (255, 255, 0)
    Blue = (0, 0, 255)
    Red = (255, 0, 0)
    White = (255,255,255)
    Nothing = (0,0,0)
    Pink = (255,105, 180)
    Orange = (255,165, 0)

class DisplayManager(object):
    def __apple(self):
        G = Colors.Green.value
        N = Colors.Nothing.value
        Y = Colors.Yellow.value
        logo = [
        N, N, N, N, Y, Y, N, N,
        N, N, N, Y, Y, N, N, N,
        N, N, G, G, G, G, N, N,
        N, G, G, G, G, G, G, N,
        N, G, G, G, G, G, G, N,
        N, G, G, G, G, G, G, N,
        N, G, G, G, G, G, G, N,
        N, N, G, G, G, G, N, N,
        ]
        return logo

    def __raspberry(self):
        G = Colors.Green.value
        N = Colors.Nothing.value
        R = Colors.Red.value
        logo = [
        N, G, G, N, N, G, G, N, 
        N, N, G, G, G, G, N, N,
        N, N, R, R, R, R, N, N, 
        N, R, R, R, R, R, R, N,
        R, R, R, R, R, R, R, R,
        R, R, R, R, R, R, R, R,
        N, R, R, R, R, R, R, N,
        N, N, R, R, R, R, N, N,
        ]
        return logo

    def __banana(self):
        N = Colors.Nothing.value
        Y = Colors.Yellow.value
        logo = [
        N, N, Y, Y, N, N, N, N,
        N, Y, Y, Y, N, N, N, N,
        Y, Y, Y, N, N, N, N, N,
        Y, Y, Y, N, N, N, N, N,
        N, Y, Y, Y, N, N, N, N,
        N, N, Y, Y, Y, N, N, N,
        N, N, N, Y, Y, Y, Y, N, 
        N, N, N, N, N, Y, Y, Y,
        ]
        return logo

    def __orange(self):
        N = Colors.Nothing.value
        O = Colors.Orange.value
        logo = [
        N, N, N, O, O, N, N, N, 
        N, O, O, O, O, O, O, N, 
        N, O, O, O, O, O, O, N, 
        O, O, O, O, O, O, O, O, 
        O, O, O, O, O, O, O, O, 
        N, O, O, O, O, O, O, N, 
        N, O, O, O, O, O, O, N, 
        N, N, N, O, O, N, N, N,  
        ]
        return logo

    def __lemon(self):
        N = Colors.Nothing.value
        Y = Colors.Yellow.value
        logo = [
        N, N, N, N, N, N, N, N,
        N, N, N, Y, Y, N, N, N,
        N, N, Y, Y, Y, Y, N, N,
        Y, Y, Y, Y, Y, Y, Y, Y,
        Y, Y, Y, Y, Y, Y, Y, Y,
        N, Y, Y, Y, Y, Y, Y, N,
        N, N, Y, Y, Y, Y, N, N,
        N, N, N, Y, Y, N, N, N,  
        ]
        return logo

    def __unknown(self):
        N = Colors.Nothing.value
        R = Colors.Red.value
        logo = [
        N, N, N, R, R, N, N, N,
        N, N, R, N, N, R, N, N,
        N, R, N, N, N, N, R, N,
        N, R, N, N, N, N, R, N,
        N, N, R, N, N, R, N, N,
        N, N, N, N, R, N, N, N,
        N, N, N, N, N, N, N, N,
        N, N, N, N, R, N, N, N,
        ]
        return logo

    def __init__(self):
        self.s = SenseHat()
        self.s.low_light = True
        self.__displayImage(self.__raspberry())#Flash the raspberry pi logo at initialization
        time.sleep(1)
        self.s.clear()

    def __displayImage(self, image):
        self.s.set_pixels(image)

    def displayImage(self, strImage):
        print("Displaying " + strImage)
        if 'apple' in strImage.lower():
            self.__displayImage(self.__apple())
        elif 'rasp' in strImage.lower():
            self.__displayImage(self.__raspberry())
        elif 'banana' in strImage.lower():
            self.__displayImage(self.__banana())
        elif 'orange' in strImage.lower():
            self.__displayImage(self.__orange())
        elif 'orange' in strImage.lower():
            self.__displayImage(self.__lemon())
        elif 'none' in strImage.lower():
            self.s.clear()
        else:
            self.__displayImage(self.__unknown())
            self.s.clear()

