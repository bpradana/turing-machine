xres = 720;
yres = 400;
sqsize = 40;
xpad = 140;
ypad = 50;
var arrTape;
var step = 0;
var tapes = [];
var tapeCount;

function preload() {
    arrTape = loadJSON("./temp.json");
}

function setup() {
    var mycanvas = createCanvas(xres, yres);
    frameRate(6);

    tapeCount = arrTape.input.length;
    for (let i = 0; i < tapeCount; i++) {
        temp = new tape(i + 1, arrTape.input[i]);
        tapes.push(temp);
    }
    print(tapes)
    mycanvas.parent('canvas');
}

function draw() {
    background(255);
    for (let i = 0; i < tapeCount; i++) {
        tapes[i].show();
    }

    print(step);
    if (step < Object.keys(arrTape.step).length) {
        step = updateTape(step);
    } else {
        noLoop()
    }

}

function updateTape(step) {
    this.step = step;
    for (let i = 0; i < tapeCount; i++) {
        tapes[i].update(arrTape.step[this.step].new_symbol[i], arrTape.step[this.step].move[i]);
    }

    this.step++;
    print('\n');
    return this.step;

}



class tape {

    constructor(tapeNum, arr) {
        if (arr != null) {
            this.currentArr = arr;
        } else {
            this.currentArr = ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_"];
        }

        this.tapeNum = tapeNum;
        this.yloc = this.tapeNum * ypad * 2;
        this.headTape = 1;
        this.headScreen = 1;
        this.screenOffset = 0;
    }

    update(newSym, move) {
        //print(this.headTape, this.headScreen);
        this.currentArr[this.headTape] = newSym;
        print(this.headTape, this.headScreen);
        if (move == ">" && this.headScreen < 9) {
            this.headTape++;
            this.headScreen++;
            print("case1");
        } else if (move == "<" && this.headScreen > 1) {
            this.headTape--;
            this.headScreen--;
            print("case2");
        } else if (move == ">" && this.headScreen == 9) {
            if (this.headTape == this.currentArr.length - 1) {
                this.currentArr.push("_");
            }
            this.screenOffset++;
            this.headTape++;
            print("case3");
        } else if (move == "<" && this.headScreen == 1) {
            if (this.headTape == 1) {
                this.currentArr.unshift("_");
            } else {
                this.headTape--;
                this.screenOffset--;
            }

            print("case4");
        }

    }
    slide(screenMove) {
        if (screenMove == ">") {
            this.currentArr.unshift("_");
            this.screenOffset--;
        } else if (screenMove == "<") {
            this.currentArr.push("_");
            this.screenOffset++;
        }


    }
    show() {
        //tape symbols
        for (let i = 0; i < 11; i++) {
            strokeJoin(ROUND);
            strokeWeight(3);
            stroke(0);
            fill(260);
            square(i * sqsize + xpad, this.yloc, sqsize);
        }
        strokeWeight(1);
        textAlign(CENTER);
        textSize(24);
        fill(0);
        for (let i = 0; i < 11; i++) {
            text(this.currentArr[i + this.screenOffset], i * sqsize + xpad + 20, this.yloc + sqsize - 10);
        }

        //tape head
        fill(250);
        strokeWeight(3);
        triangle(this.headScreen * sqsize + xpad, this.yloc - 30, this.headScreen * sqsize + xpad + 20, this.yloc - 5, this.headScreen * sqsize + xpad + 40, this.yloc - 30);
    }
}
