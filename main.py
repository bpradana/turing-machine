import json


class TuringMachine:
    def __init__(self, code):
        self.code = json.load(open(code))
        self.init = self.code['init']
        self.accept = self.code['accept']
        self.transition = self.code['transition']

    def check(self, input_string):
        pass


if __name__ == '__main__':
    file_name = 'transition.json'
    tm = TuringMachine(file_name)