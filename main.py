from TuringMachine import TuringMachine
from TuringMachine import Tapes
import os
import json

if __name__ == '__main__':
    while True:
        program_list = os.listdir('program')
        print('\n-------------------------')
        for i, program in sorted(enumerate(program_list)): print(i+1, program)
        print('-------------------------')

        try:
            PROGRAM = program_list[int(input('Program\t: '))-1]
            INPUT_STRING = input('Input\t: ')
            
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
