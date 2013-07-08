#!/usr/bin/python3

from flask import Flask, render_template, request
import solver
import re

app = Flask(__name__)

@app.route('/')
def view():
    return render_template('input.html', lettervals=solver.LETTER_VALS)

@app.route('/solve', methods=['GET', 'POST'])
def solve():
    if request.method == 'POST':
        line = request.form['input'].strip().lower()
        if not solver.valid(line):
            return render_template('badinput.html')
        words, board, mults = solver.solve(line)
        data = { 'words': [ x.__dict__ for x in words],
                'board': ''.join(board),
                'mults': [ {0: '', 1: 'DW', 2: 'TW', 3: 'DL', 6: 'TL',}[i] for i in mults],
                'lettervals': solver.LETTER_VALS,
                }

        return render_template('viewer.html', **data)
        #return render_template('viewer.html', words=[ x.__dict__ for x in [solver.Word("apple", 50, [1,3,14]), solver.Word("banana", 10, [1,5,10,15,2])]], board=''.join(board), mults=['','','','','','','','','','','','','','','','DL'], lettervals=solver.LETTER_VALS)
    elif request.method == 'GET':
        return render_template('badinput.html')



if __name__ == "__main__":
    app.run(debug=True)
    #app.run()
