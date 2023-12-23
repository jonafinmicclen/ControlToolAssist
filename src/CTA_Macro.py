#save, load, create featrures

from datetime import datetime
import pickle
import threading
import time
from inputs import get_gamepad
from PIL import Image
import pyautogui
import base64

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
        self.ScreenStates = []

        self.recording = False

        self.ControllerPollingT = 1/1000 #These should get from config file 
        self.ScreenPollingT = 1/1

        if path==None:
            dateAndTime = str(datetime.now())
            dateAndTime = dateAndTime.replace(':','.')
            self.path = f'saves/{dateAndTime}.pkl'
        else:
            self.path = path

    def start_recording(self):

        self._record_screen_thread = threading.Thread(target=self._recording_screen)
        self._record_screen_thread.daemon = True
        self._record_screen_thread.start()

        self._record_controller_thread = threading.Thread(target=self._recording_controller)
        self._record_controller_thread.daemon = True
        self._record_controller_thread.start()

        self.recording = True

    def stop_recording(self):
        self.recording = False

    def _recording_controller(self):
        while self.recording == True:
            time.sleep(self.ControllerPollingT)
            events = get_gamepad()

            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY.append(event.state)
                elif event.code == 'ABS_X':
                    self.LeftJoystickX.append(event.state)
                elif event.code == 'ABS_RY':
                    self.RightJoystickY.append(event.state)
                elif event.code == 'ABS_RX':
                    self.RightJoystickX.append(event.state)
                elif event.code == 'ABS_Z':
                    self.LeftTrigger.append(event.state)
                elif event.code == 'ABS_RZ':
                    self.RightTrigger.append(event.state)
                elif event.code == 'BTN_TL':
                    self.LeftBumper.append(event.state)
                elif event.code == 'BTN_TR':
                    self.RightBumper.append(event.state)
                elif event.code == 'BTN_SOUTH':
                    self.A.append(event.state)
                elif event.code == 'BTN_NORTH':
                    self.X.append(event.state)
                elif event.code == 'BTN_WEST':
                    self.Y.append(event.state)
                elif event.code == 'BTN_EAST':
                    self.B.append(event.state)
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb.append(event.state)
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb.append(event.state)
                elif event.code == 'BTN_SELECT':
                    self.Back.append(event.state)
                elif event.code == 'BTN_START':
                    self.Start.append(event.state)
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad.append(event.state)
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad.append(event.state)
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad.append(event.state)
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad.append(event.state)
    
    def _recording_screen(self):
        while self.recording == True:
            time.sleep(self.ScreenPollingT)

            screenshot_data = pyautogui.screenshot().tobytes()
            screenshot_encoded = base64.b64encode(screenshot_data).decode('utf-8')
            self.ScreenStates.append(screenshot_encoded)

    def save(self):
        if self.recording == True:
            raise Exception('Cannot save while recording')
        else:
            self._record_screen_thread = None
            self._record_controller_thread = None
            
            with open(self.path, "wb") as file:
                pickle.dump(self, file)

    @classmethod
    def load(cls, filename):
        with open(filename, "rb") as file:
            return pickle.load(file)

newMacro = CTA_Macro()
newMacro.start_recording()
time.sleep(3)
newMacro.stop_recording()
newMacro.save()
print(newMacro.path)