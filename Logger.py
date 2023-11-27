import Controllers
import numpy

class ControllerLogger():
    
    def __init__(self, controller_type):
        
        self.controller_type = controller_type
        #0 type is xbox
        if self.controller_type == 0:
            self.controller = Controllers.XboxController()