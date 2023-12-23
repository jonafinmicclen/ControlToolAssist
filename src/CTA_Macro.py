#save, load, create featrures

from datetime import datetime
import pickle

class CTA_Macro:

    def __init__(self, path=None):

        self.LeftJoystickY = []
        self.LeftJoystickX = []
        self.RightJoystickY = []
        self.RightJoystickX = []
        self.LeftTrigger = []
        self.RightTrigger = []
        self.LeftBumper = []
        self.RightBumper = []
        self.A = []
        self.X = []
        self.Y = []
        self.B = []
        self.LeftThumb = []
        self.RightThumb = []
        self.Back = []
        self.Start = []
        self.LeftDPad = []
        self.RightDPad = []
        self.UpDPad = []
        self.DownDPad = []

        if path==None:
            dateAndTime = str(datetime.now())
            dateAndTime = dateAndTime.replace(':','.')
            self.path = f'saves/{dateAndTime}.pkl'
        else:
            self.path = path

    def save(self):
        with open(self.path, "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, filename):
        with open(filename, "rb") as file:
            return pickle.load(file)
