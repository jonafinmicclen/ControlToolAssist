#save, load, create featrures

from datetime import datetime
import pickle
import threading
import time
from inputs import get_gamepad
from PIL import Image
import pyautogui
from Macro import Controller
import utilities

class MacroTool:

    def __init__(self, controller_polling_T, screen_polling_T, path=None):

        # Recordings
        self.controller_states = []
        self.screen_states = []
        self.controller_samples = 0
        self.screen_samples = 0
        
        # Threads
        self._record_screen_thread = None
        self._record_controller_thread = None
        self._passthrough_thread = None
        # Thread flags
        self.recording = False
        self.playing = False
        self.passthrough = False
        
        # Polling rate config
        self.controller_polling_T = controller_polling_T
        self.passthrough_delay = controller_polling_T
        self.screen_polling_T = screen_polling_T
        
        self.virtual_controller = Controller.VirtualController()
        self.real_controller = Controller.XboxController()

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
        self.recording_start_time = time.time()
        self.recording = True
        self._record_controller_thread = threading.Thread(target=self._recording_controller)
        self._record_controller_thread.daemon = True
        self._record_controller_thread.start()


    def stop_recording(self):

        self.recording = False
        self._record_controller_thread.join()
        self._record_screen_thread.join()

    def _recording_controller(self):

        while self.recording:

            time_taken = utilities.elapsed_time_from_function(self.snapshot_controller_state())
            time.sleep(self.controller_polling_T - time_taken)
            
        
    def snapshot_controller_state(self):

        controllerState = self.real_controller.read()
        self.controller_states.append([controllerState, time.time() - self.recording_start_time])
        self.controller_samples+=1
    
    def _recording_screen(self):

        while self.recording == True:

            time_taken = utilities.elapsed_time_from_function(self.snapshot_screen())
            time.sleep(self.screen_polling_T - time_taken)

    def snapshot_screen(self):

        self.screen_states.append([pyautogui.screenshot().tobytes(), time.time()-self.recording_start_time])
        self.screen_samples += 1
        
    def _passthrough(self):
        
        while self.passthrough:

            if not self.playing:
                time_taken = utilities.elapsed_time_from_function(self.virtual_controller.play(), self.real_controller.read())

            time.sleep(self.controller_polling_T - time_taken)
            
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

            self.virtual_controller.play(self.controller_states[samplesN][0])
            samplesN += 1
            time.sleep(self.controller_polling_T)

        self.virtual_controller.controller.reset()
        self.virtual_controller.controller.update()
        self.playing = False

    def save(self):
        if self.recording == True:
            raise Exception('Cannot save while recording')
        else:
            #Exclude non-necessary attributes from saving
            self._record_screen_thread = None
            self._record_controller_thread = None
            self._playing_thread = None
            self.virtual_controller = None ##This will cause error when playback from loaded in macro

            with open(self.path, "wb") as file:
                pickle.dump(self, file)

    @classmethod
    def load(cls, filename):
        with open(filename, "rb") as file:
            return pickle.load(file)
        
        
