import json
import time


class TuringMachine:
    def __init__(self, code, padding=10):
        self.code = json.load(open(code))
        self.init = self.code['init']
        self.accept = self.code['accept']
        self.transitions = self.code['transitions']
        self.padding = ['_' for _ in range(padding)]
        self.tape_head = padding

    def check(self, input_string, padding='center'):
        start_time = time.time()
        if padding == 'center':
            input_string = self.padding + list(input_string) + self.padding
            current_tape_head = self.tape_head

        if padding == 'left':
            input_string = self.padding*2 + list(input_string)
            current_tape_head = self.tape_head*2

        if padding == 'right':
            input_string = list(input_string) + self.padding*2
            current_tape_head = 0

        current_state = self.init
        
        original = input_string.copy()

        print('Current State: %s' % current_state)
        print(' '.join(input_string))
        print(' '.join(['^' if _ == current_tape_head else ' ' for _ in range(len(input_string))]))

        while current_state not in self.accept:
            try:
                current_transition = self.transitions[current_state][input_string[current_tape_head]]
                current_state = current_transition[0]
            except:
                print('=== TRANSITION ERROR ===')
                break

            try:
                input_string[current_tape_head] = current_transition[1]
            except:
                print('=== TAPE LENGTH EXCEEDED ===')
                break

            if current_transition[2] == 'R':
                current_tape_head += 1
            if current_transition[2] == 'L':
                current_tape_head -= 1
            if current_transition[2] == '-':
                current_tape_head = current_tape_head
            
            print('Current State: %s' % current_state)
            print(' '.join(input_string))
            print(' '.join(['^' if _ == current_tape_head else ' ' for _ in range(len(input_string))]))
        
        end_time = time.time()

        if current_state in self.accept:
            print('=== ACCEPTED ===')
            print('input  : %s' % ''.join(original))
            print('output : %s' % ''.join(input_string))
            print('finished in %.3f seconds' % (end_time-start_time))


if __name__ == '__main__':
    file_name = 'transition.json'
    input_string = '00000100001'

    tm = TuringMachine(file_name)
    tm.check(input_string, padding='right')