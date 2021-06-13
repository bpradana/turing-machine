from flask import Flask
from flask import request


app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    from TuringMachine import TuringMachine
    from TuringMachine import Tapes
    import json
    
    PATH = 'program/'
    TAPE_COUNT = request.json['tape_count']
    PROGRAM = PATH + request.json['program']
    INPUT_STRING = request.json['input']

    tm = TuringMachine()
    tapes = Tapes(TAPE_COUNT)
    tapes.load_input(INPUT_STRING)

    tm.load_tapes(tapes)
    tm.load_program(PROGRAM)
    log_list = tm.run(verbose=False, log=True)

    return json.dumps(log_list)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
