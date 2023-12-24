import configparser

class Config:

    def __init__(self):

        self.config_file_path = 'config/config.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file_path)

        self.controler_polling_rate = 1/(self.config.getint('General','ControllerPollingRate'))
        self.screen_polling_rate = 1/(self.config.getint('General','ScreenClippingRate'))

