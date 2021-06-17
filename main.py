from flask import Flask
from flask import request


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        from TuringMachine import TuringMachine
        from TuringMachine import Tapes
        import json
        
        PATH = 'program/'
        PROGRAM = PATH + request.json['program']
        INPUT_STRING = request.json['input']

        tm = TuringMachine()
        tm.load_program(PROGRAM)

        tapes = Tapes(tm.program['tape_count'])
        tapes.load_input(INPUT_STRING)
        tm.load_tapes(tapes)

        log_list = tm.run(verbose=False, log=True)

        return json.dumps(log_list)
    if request.method == 'GET':
        from os import listdir
        import json

        program_list = listdir('program')
        return json.dumps(program_list)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
