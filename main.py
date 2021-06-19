from TuringMachine import TuringMachine
from TuringMachine import Tapes
import os
import json

if __name__ == '__main__':
    while True:
        print('\n-------------------------')
        for program in os.listdir('program'): print(program)
        print('-------------------------')
        PROGRAM = input('Program\t: ')
        INPUT_STRING = input('Input\t: ')

        try:
            tm = TuringMachine()
            tm.load_program('program/' + PROGRAM)

            tapes = Tapes(tm.program['tape_count'])
            tapes.load_input(INPUT_STRING)
            tm.load_tapes(tapes)

            data = tm.run(verbose=True, log=True)

            with open('public/temp.json', 'w') as outfile:
                json.dump(data, outfile)

        except Exception as e:
            print(e)
