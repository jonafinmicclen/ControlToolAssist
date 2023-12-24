import math
import threading
from inputs import get_gamepad
import vgamepad

class XboxController:

    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self):

        lsx = self.LeftJoystickX
        lsy = self.LeftJoystickY
        rsx = self.RightJoystickX
        rsy = self.RightJoystickY

        lt = self.LeftTrigger
        rt = self.RightTrigger

        lb = self.LeftBumper
        rb = self.RightBumper

        ba = self.A
        bx = self.X 
        by = self.Y
        bb = self.B

        return [lsx,lsy,rsx,rsy,lt,rt,lb,rb,ba,bx,by,bb]

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_WEST':
                    self.X = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state

class VirtualController():

    def __init__(self):
        
        self.controller = vgamepad.VX360Gamepad()
        self.current_state = [0,0,0,0, 0, 0, 0, 0, 0, 0, 0, 0]

    def play(self, state):
        
        self.controller.left_joystick_float(x_value_float=state[0], y_value_float=state[1])
        self.controller.right_joystick_float(x_value_float=state[2],y_value_float=state[3])

        self.controller.left_trigger_float(value_float=state[4])
        self.controller.right_trigger_float(value_float=state[5])

        if state[6] == 1:
            self.controller.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        else:
            self.controller.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)

        self.controller.update()
        self.current_state = state