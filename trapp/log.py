# -*- coding: utf-8 -*-


class Log():

    def __init__(self, name):
        self.name = name
        self.file = open(name, 'w')
        return None

    def message(self, msg):
        return self.file.write(msg + '\n')

    def end(self):
        self.file.close()
        self.file = None
        return self.file
