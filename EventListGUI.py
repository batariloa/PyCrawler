class EventList(list):

    def __init__(self, window):
        super(list, self).__init__()
        self.window = window

    def __setitem__(self, key, value):
        super(EventList, self).__setitem__(key, value)
        print("The list has been changed!")

    def __delitem__(self, value):
        super(EventList, self).__delitem__(value)
        print("The list has been changed!")

    def __add__(self, value):
        super(EventList, self).__add__(value)
        print("The list has been changed!")

    def __iadd__(self, value):
        super(EventList, self).__iadd__(value)
        print("The list has been changed!")

    def append(self, value):
        super(EventList, self).append(value)
        current_result = value
        self.window['-WEBSITE LIST-'].update(
            current_result.keys())

    def remove(self, value):
        super(EventList, self).remove(value)
