class CallBackPool():
    events = {}

    def add(self, name, func):
        self.events[name] = func

    def call(self, name, arg = None):
        if name not in self.events.keys():
            return -1
        return self.events[name](arg)


