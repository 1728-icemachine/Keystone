class CallBackPool():
    events = {}

    def add(self, name, func):
        events[name] = func

    def call(self, name, arg = None):
        if name not in events.keys():
            return -1
        return events[name](arg)


