from os import name
import time

class Tapes:
    '''
    Kelas untuk merepresentasikan tape pada turing machine
    '''
    def __init__(self, tape_count, tape_length=2048) -> None:
        '''
        Constructor dari kelas Tapes
        ...
        Parameter
        ---------
        tape_count: int
        jumlah tape yang digunakan
        tape_length: int
        panjang tape yang digunakan
        '''
        self.tape_count = tape_count
        self.tape_length = tape_length
        self.first_index = None
        self.tapes = [['_' for _ in range(tape_length)] for _ in range(tape_count)]

    def load_input(self, input_string):
        '''
        Fungsi untuk memasukkan input string ke tengah tape
        dengan (rumus panjang_tape - panjang_input) // 2
        ...
        Parameter
        ---------
        input_string: str
        string yang akan dimasukkan ke tape
        '''
        assert self.tape_length > len(input_string), '🛑 Tape length exceeded'
        print('✅ Input validation passed')

        self.first_index = (self.tape_length - len(input_string)) // 2

        for index, char in enumerate(input_string):
            self.tapes[0][index+self.first_index] = char

    def read(self, index):
        '''
        Fungsi untuk membaca karakter sesuai index
        ...
        Parameter
        ---------
        index: list
        index dari karakter pada tape
        '''
        char = list()
        for i, tape in enumerate(self.tapes):
            char.append(tape[index[i]])
        return char

    def write(self, index, char):
        '''
        Fungsi untuk menulis ke tape sesuai index
        ...
        Parameter
        ---------
        index: list
        index dari karakter pada tape
        char: list
        karakter yang akan ditulis
        '''
        for i, tape in enumerate(self.tapes):
            tape[index[i]] = char[i]

    def prettify(self):
        '''
        Fungsi untuk menampilkan tape seperlunya
        biar kevin enak bikin front end nya
        ...
        Return
        ------
        formatted: list
        tape yang sudah diformat agar mudah dibaca
        '''
        first_element = None
        last_element = None
        curr_smallest = None
        curr_largest = None

        for tape in self.tapes:
            for i, char in enumerate(tape):
                if char != '_':
                    curr_smallest = i
                    curr_largest = i
                    
                if first_element != None:
                    if first_element > curr_smallest:
                        first_element = curr_smallest
                else:
                    first_element = curr_smallest

                if last_element != None:
                    if last_element < curr_largest:
                        last_element = curr_largest
                else:
                    last_element = curr_largest

        formatted = list()
        for tape in self.tapes:
            formatted.append(tape[first_element-1:last_element+2])

        return formatted
            


class Head:
    '''
    Kelas untuk merepresentasikan head pada turing machine
    '''
    def __init__(self) -> None:
        '''
        Constructor untuk kelas Head
        '''
        self.tapes = None
        self.program = None
        self.program_name = None
        self.current_state = None
        self.final_state = None
        self.input = None
        self.output = None
        self.move = None
        self.current_index = None

    def load_program(self, program):
        '''
        Fungsi untuk memuat program ke head
        ...
        Parameter
        ---------
        program_dict: list
        list of dict program yang akan dijalankan
        '''
        self.program = program['transition']
        self.program_name = program['name']
        self.current_state = program['initial_state']
        self.final_state = program['final_state']

    def validate_program(self):
        '''
        Fungsi untuk melakukan validasi program
        '''
        for i, line in enumerate(self.program):
            assert len(line['input']) == len(line['output']) == len(line['move']), '🛑 Error on line %d' % (i+5)
        print('✅ Program validation passed')
        
    def load_tape(self, tapes):
        '''
        Fungsi untuk memuat tape
        ...
        Parameter
        ---------
        tapes: object
        object dari kelas Tapes
        '''
        self.tapes = tapes
        self.current_index = [tapes.first_index for _ in range(tapes.tape_count)]

    def get_by_state(self, program, state):
        '''
        Fungsi untuk mendapatkan perintah dari state saat itu
        ...
        Parameter
        ---------
        state: str
        state pada saat itu
        '''
        try:
            return [line for line in program if line['current_state'] == state]
        except:
            print('🛑 State not found')

    def get_by_input(self, program, input):
        '''
        Fungsi untuk mendapatkan perintah dari input saat itu
        ...
        Parameter
        ---------
        input: list
        input pada saat itu
        '''
        try:
            return [line for line in program if line['input'] == input]
        except:
            print('🛑 State not found')

    def assign_move(self):
        '''
        Fungsi untuk mengubah index berdasarkan move
        '''
        for index, move in enumerate(self.move):
            if move == '<':
                self.current_index[index] -= 1
            if move == '>':
                self.current_index[index] += 1
            if move == '-':
                self.current_index[index] = self.current_index[index]

    def check(self):
        '''
        Fungsi untuk melakukan check pada kondisi saat ini
        ...
        Return
        ------
        finished: boolean
        status turing machine saat itu (selesai atau belum)
        '''
        if self.current_state in self.final_state:
            print('✅ Finished')
            return True

        self.input = self.tapes.read(self.current_index)
        try:
            filtered_program = self.get_by_state(self.program, self.current_state)
            filtered_program = self.get_by_input(filtered_program, self.input)
            filtered_program = filtered_program[0]
        except:
            print('🛑 Transition error! Input %s at %s with current state %s' % (self.input, self.current_index, self.current_state))
            return True
        
        self.current_state = filtered_program['next_state']
        self.move = filtered_program['move']
        self.output = filtered_program['output']

        self.tapes.write(self.current_index, self.output)
        self.assign_move()


class TuringMachine:
    def __init__(self) -> None:
        '''
        Kelas untuk merepresentasikan turing machine
        '''
        self.program = None
        self.tapes = None
        self.head = None

    def load_program(self, file_name):
        '''
        Fungsi untuk memuat program
        ...
        Parameter
        ---------
        file_name: str
        nama file program yang akan dimuat
        '''
        with open(file_name) as f:
            raw_text = f.read()

        temp_split = raw_text.split('---\n')

        meta = temp_split[0]
        transition = temp_split[1]

        meta = meta.split('\n')
        transition = transition.split('\n')
        transition = [line.split(' ') for line in transition]
        
        program = {
            'name': meta[0],
            'initial_state': meta[1],
            'final_state': meta[2].split(','),
            'tape_count': int(meta[3]),
            'transition': list(),
        }

        for line in transition:
            line_dict = {
                'current_state': line[0],
                'input': line[1].split(','),
                'next_state': line[2],
                'output': line[3].split(','),
                'move': line[4].split(','),
            }
            program['transition'].append(line_dict)

        self.program = program
        print('✅ Program \'%s\' loaded' % self.program['name'])

    def load_tapes(self, tapes):
        '''
        Fungsi untuk memuat tape
        ...
        Parameter
        ---------
        tapes: object
        object dari kelas Tapes
        '''
        self.tapes = tapes
        print('✅ %d tapes loaded' % self.tapes.tape_count)

    def verbose_print(self):
        print('State:\t', self.head.current_state)
        for i, tape in enumerate(self.tapes.prettify()):
            print('Tape %d:\t%s' % (i+1,''.join(tape)))
        print()

    def run(self, verbose=False, log=False):
        '''
        Fungsi untuk menjalankan turing machine dan
        mengembalikan log jalannya program
        '''
        self.head = Head()
        self.head.load_tape(self.tapes)
        self.head.load_program(self.program)
        self.head.validate_program()
        print('🔥 Running program')

        log_list = list()

        finished = False
        start =  time.time()

        while not finished:
            if verbose:
                self.verbose_print()
            finished = self.head.check()

            if log:
                log = {
                    'tapes': self.tapes.prettify(),
                    'state': self.head.current_state,
                    'move': self.head.move,
                }
                log_list.append(log)

        print('🕖 Took %.4f seconds' % (time.time() - start))
        return log_list
