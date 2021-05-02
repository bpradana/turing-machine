import json


class TuringMachine:
    def __init__(self, code, padding=10):
        self.code = json.load(open(code))
        self.init = self.code['init']
        self.accept = self.code['accept']
        self.transitions = self.code['transitions']
        self.padding = ['_' for _ in range(padding)]
        self.tape_head = padding

    def check(self, input_string):
        input_string = self.padding + list(input_string) + self.padding
        current_state = self.init
        current_tape_head = self.tape_head
        
        print('Current State: %s' % current_state)
        print(' '.join(input_string))
        print(' '.join(['^' if _ == current_tape_head else ' ' for _ in range(len(input_string))]))

        while current_state not in self.accept:
            current_transition = self.transitions[current_state][input_string[current_tape_head]]
            current_state = current_transition[0]
            input_string[current_tape_head] = current_transition[1]
            if current_transition[2] == 'R':
                current_tape_head += 1
            if current_transition[2] == 'L':
                current_tape_head -= 1
            if current_transition[2] == '-':
                current_tape_head = current_tape_head
            
            print('Current State: %s' % current_state)
            print(' '.join(input_string))
            print(' '.join(['^' if _ == current_tape_head else ' ' for _ in range(len(input_string))]))

        if current_state in self.accept:
            print('ACCEPTED')


if __name__ == '__main__':
    file_name = 'transition.json'
    input_string = '00010001'

    tm = TuringMachine(file_name)
    tm.check(input_string)