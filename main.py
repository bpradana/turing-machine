from flask import Flask
from flask import request


app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    from TuringMachine import TM
    import json

    PATH = 'program/'
    CODE = PATH + request.json['mode'] + '.json'
    INPUT_STRING = request.json['input']

    TM = TM()
    TM.construct(CODE, 1)
    try:
        output = TM.run(INPUT_STRING)
        return json.dumps(output)
    except:
        return 'Error', 400


if __name__ == '__main__':
    app.run(debug=True)
