import json


class Tape:
    def __init__(self):
        self.code = None        # Load JSON

        self.name = None        # Program Name
        self.init = None        # Initial State 
        self.accept = None      # Accepting States
        self.transitions = None # Transitions

        self.tape = ['_', '_', '_']

        self.current_state = self.init  # Current State
        self.current_position = 1       # Current Head Position
        self.current_transition = None  # Current Transition

    def load_program(self, code, tape_index):
        self.code = json.load(open(code))                       # Load JSON
        self.name = self.code['name']                           # Program Name
        self.init = self.code['init']                           # Initial State 
        self.accept = self.code['accept']                       # Accepting States
        self.transitions = self.code['transitions'][tape_index] # Transitions
        self.current_state = self.init                          # Current Transition

    def load_tape(self, input_string):
        self.tape = list('_' + input_string + '_')

    def check(self):
        try:
            self.tape[self.current_position]
        except:
            if self.current_transition[2] == 'R':
                self.tape.append('_')
            elif self.current_transition[2] == 'L':
                self.tape.insert(0, '_')

        try:
            self.current_transition = self.transitions[self.current_state][self.tape[self.current_position]]
            self.current_state = self.current_transition[0]
        except:
            print('Rejected, %s not in %s' % (self.tape[self.current_position-1], self.current_state))

        try:
            self.tape[self.current_position] = self.current_transition[1]
        except:
            print('Rejected')

        if self.current_transition[2] == 'R':
            self.current_position += 1
        if self.current_transition[2] == 'L':
            self.current_position -= 1
        if self.current_transition[2] == '-':
            self.current_position = self.current_position

        if self.current_state in self.accept:
            return True

        self.collect_garbage()

    def collect_garbage(self):
        if self.tape[1] == '_':
            self.tape.pop(0)
            self.current_position -= 1
        if self.tape[-1] != '_':
            self.tape.append('_')


class TM:
    def __init__(self):
        self.tapes = list()

    def construct(self, code, tape_count):
        for i in range(tape_count):
            self.tapes.append(Tape())

        for tape_index, tape in enumerate(self.tapes):
            tape.load_program(code, tape_index)

    def prettify(self, input_string):
        pass

    def run(self, input_string):
        self.tapes[0].load_tape(input_string)

        output = []

        while True:

            data_structure = {
                'tape': [],
                'transition': [],
                'head': 0,
            }

            for tape_index, tape in enumerate(self.tapes):
                status = tape.check()
                data_structure['tape'].append(tape.tape.copy())
                data_structure['transition'].append(tape.current_transition.copy())
                data_structure['head'] = tape.current_position

                if tape_index==len(self.tapes)-1 and status:
                    break

            output.append(data_structure)

            if status:
                break
        
        return output