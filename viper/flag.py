class Flag:
    def __init__(self, name, value, usage):
        self.name = name
        self.value = value
        self.usage = usage

    def doc(self):
        return ' :param {}: {}'.format(self.name, self.usage)
