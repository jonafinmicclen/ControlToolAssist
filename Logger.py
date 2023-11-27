import Controllers
import numpy

#Default values
log_rate_ms = 300
controller_type = 0

class ControllerLogger():
    
    def __init__(self, controller_type, log_rate_ms):
        
        self.controller_type = controller_type
        self.log_rate_ms = log_rate_ms
        
        #0 type is xbox
        if self.controller_type == 0:
            self.controller = Controllers.XboxController()