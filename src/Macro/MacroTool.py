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

    def _recording_controller(self):

        samplesN = 0
        startTime = time.time()
        controller = Controller.XboxController()

        while self.recording == True:
            elapsedTime = time.time() - startTime
            if elapsedTime >= self.ControllerPollingT*samplesN:
                
                controllerState = controller.read()
                self.ControllerStates.append([controllerState, elapsedTime])
                samplesN+=1
            
        self.ControllerSamples = samplesN
    
    def _recording_screen(self):

        startTime = time.time()
        samplesN = 0

        while self.recording == True:
            elapsedTime = time.time()-startTime
            if elapsedTime >= self.ScreenPollingT*samplesN:

                self.ScreenStates.append([pyautogui.screenshot().tobytes(), elapsedTime])
                samplesN+=1
        
        self.ScreenSamples = samplesN

    def play(self):
        
        self._playing_thread = threading.Thread(target=self._playing)
        self._playing_thread.daemon = True
        self._playing_thread.start()

    def _playing(self):
        
        startTime = time.time()
        samplesN = 0
        virtualController = Controller.VirtualController()

        while samplesN< self.ControllerSamples:
            elapsedTime = time.time()-startTime
            if elapsedTime >= self.ControllerStates[samplesN][1]:

                virtualController.play(self.ControllerStates[samplesN][0])
                samplesN += 1

    def save(self):
        if self.recording == True:
            raise Exception('Cannot save while recording')
        else:
            #Exclude non-necessary attributes from saving
            self._record_screen_thread = None
            self._record_controller_thread = None

            with open(self.path, "wb") as file:
                pickle.dump(self, file)

    @classmethod
    def load(cls, filename):
        with open(filename, "rb") as file:
            return pickle.load(file)

if __name__ == '__main__':
    
    newMacro = MacroTool()
    newMacro.start_recording()
    time.sleep(10)
    print(newMacro.path)
    newMacro.stop_recording()
    newMacro.save()

    loadedMacro = MacroTool.load(newMacro.path)
    print(loadedMacro.ScreenStates)
    screenshot = loadedMacro.ScreenStates[0]
    image = Image.frombytes('RGB',(1920,1080),screenshot)
    image.show()
