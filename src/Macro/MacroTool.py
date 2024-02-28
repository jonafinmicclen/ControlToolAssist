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

        # Recordings
        self.controller_states = []
        self.screen_states = []
        self.controller_samples = 0
        
        # Threads
        self._record_screen_thread = None
        self._record_controller_thread = None
        self._passthrough_thread = None

        # Thread flags
        self.recording = False
        self.playing = False
        self.passthrough = False
        
        # Polling rate config
        self.ControllerPollingT = ControllerPollingT
        self.passthrough_delay = ControllerPollingT
        self.ScreenPollingT = ScreenPollingT
        
        self.vController = Controller.VirtualController()
        self.controller = Controller.XboxController()

        if path==None:
            dateAndTime = str(datetime.now())
            dateAndTime = dateAndTime.replace(':','.')
            self.path = f'saves/{dateAndTime}.pkl'
        else:
            self.path = path

    def start_recording(self):

        # Record screen state
        self._record_screen_thread = threading.Thread(target=self._recording_screen)
        self._record_screen_thread.daemon = True
        self._record_screen_thread.start()

        # Record controller state
        self.startTime = time.time()
        self.recording = True
        self._record_controller_thread = threading.Thread(target=self._recording_controller)
        self._record_controller_thread.daemon = True
        self._record_controller_thread.start()


    def stop_recording(self):

        self.recording = False
        self._record_controller_thread.join()
        self._record_screen_thread.join()

    def _recording_controller(self):

        while self.recording and not self.passthrough:

            self.snapshot_controller_state()
            time.sleep(self.ControllerPollingT)
            
        
    def snapshot_controller_state(self):

        controllerState = self.controller.read()
        self.controller_states.append([controllerState, time.time() - self.startTime])
        self.controller_samples+=1
    
    def _recording_screen(self):

        startTime = time.time()
        samplesN = 0

        while self.recording == True:

            self.screen_states.append([pyautogui.screenshot().tobytes(), time.time()-startTime])
            samplesN+=1

            time.sleep(self.ScreenPollingT)
        
        self.ScreenSamples = samplesN
        
    def _passthrough(self):
        
        while self.passthrough:

            if not self.playing:
                self.vController.play(self.controller.read())

            if self.recording:
                self.snapshot_controller_state()

            time.sleep(self.passthrough_delay)
            
    def start_pasthrough(self):
        self.passthrough = True
        self._passthrough_thread = threading.Thread(target=self._passthrough)
        self._passthrough_thread.daemon = True
        self._passthrough_thread.start()
        
    def stop_passthrough(self):
        
        self.passthrough = False
        self._passthrough_thread.join()
            
    def play(self):
        
        self._playing_thread = threading.Thread(target=self._playing)
        self._playing_thread.daemon = True
        self._playing_thread.start()
        self.playing = True

    def _playing(self):

        samplesN = 0

        while samplesN< self.controller_samples:

            self.vController.play(self.controller_states[samplesN][0])
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
        
        
