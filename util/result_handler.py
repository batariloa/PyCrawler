from my_enum.gui_variables import WindowVariables as wv


class ResultHandler():

    def __init__(self, window):
        self.window = window
        self.current_result = None
        self.stopFlag = False
        self.pauseFlag = False

    def append(self, value):
        self.current_result = value
        self.window[wv.list_of_websites].update(
            self.current_result.keys())

    def getResult(self):
        self.current_result

    def stop(self):
        self.stopFlag = True

    def pause(self):
        self.pauseFlag = True

    def resume(self):
        self.pauseFlag = False
        self.stopFlag = False
