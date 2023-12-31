#save, load, create featrures

from datetime import datetime
import pickle
import threading
import time
from inputs import get_gamepad
from PIL import Image
import pyautogui
from Macro import Controller

class MacroTool:

    def __init__(self, ControllerPollingT, ScreenPollingT, path=None):

        self.ControllerStates = []
        self.ScreenStates = []

        self.recording = False
        self.playing = False
        
        self.ControllerPollingT = ControllerPollingT
        self.ScreenPollingT = ScreenPollingT

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
        self._record_controller_thread.join()
        self._record_screen_thread.join()

    def _recording_controller(self):

        samplesN = 0
        startTime = time.time()
        controller = Controller.XboxController()

        while self.recording == True:
                
            controllerState = controller.read()
            self.ControllerStates.append([controllerState, time.time() - startTime])
            samplesN+=1

            time.sleep(self.ControllerPollingT)
            
        self.ControllerSamples = samplesN
    
    def _recording_screen(self):

        startTime = time.time()
        samplesN = 0

        while self.recording == True:

            self.ScreenStates.append([pyautogui.screenshot().tobytes(), time.time()-startTime])
            samplesN+=1

            time.sleep(self.ScreenPollingT)
        
        self.ScreenSamples = samplesN

    def play(self):
        
        self._playing_thread = threading.Thread(target=self._playing)
        self._playing_thread.daemon = True
        self._playing_thread.start()
        self.playing = True

    def _playing(self):

        samplesN = 0
        self.vController = Controller.VirtualController()

        while samplesN< self.ControllerSamples:

            self.vController.play(self.ControllerStates[samplesN][0])
            samplesN += 1
            time.sleep(self.ControllerPollingT)

        self.vController.controller.reset()
        self.vController.controller.update()
        self.playing = False

    def save(self):
        if self.recording == True:
            raise Exception('Cannot save while recording')
        else:
            #Exclude non-necessary attributes from saving
            self._record_screen_thread = None
            self._record_controller_thread = None
            self._playing_thread = None
            self.vController = None ##This will cause error when playback from loaded in macro

            with open(self.path, "wb") as file:
                pickle.dump(self, file)

    @classmethod
    def load(cls, filename):
        with open(filename, "rb") as file:
            return pickle.load(file)
        
        
