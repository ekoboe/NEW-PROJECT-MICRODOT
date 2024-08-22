#from machine import Pin

class POWERlab:
    def __init__(self, pin):
        self.pwr1 = 2

    def onPower(self):
        print("Power On")
        self.pwr1 = 1

    def offPower(self):
        print("Power Off")
        self.pwr1 = 0

    def cleanUp(self):
        print('Cleaning up pins')
