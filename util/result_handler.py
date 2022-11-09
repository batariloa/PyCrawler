class ResultHandler():

    def __init__(self, window):
        self.window = window
        self.current_result = None

    def append(self, value):
        self.current_result = value
        self.window['-WEBSITE LIST-'].update(
            self.current_result.keys())

    def getResult(self):
        self.current_result
