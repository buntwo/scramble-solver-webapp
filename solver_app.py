#!/usr/bin/python3

from flask import Flask, render_template, request
import solver
import re

app = Flask(__name__)

@app.route('/')
def view():
    return render_template('input.html')

@app.route('/solve', methods=['GET', 'POST'])
def solve():
    if request.method == 'POST':
        line = request.form['input'].strip()
        if not solver.valid(line):
            return render_template('badinput.html')
        words = solver.solve(line)
        board = re.sub(r'[/?]', '', line)
        return render_template('viewer.html', words=[ x.__dict__ for x in words], board=board)
        #return render_template('viewer.html', words=[ x.__dict__ for x in [solver.Word("apple", 50, [1,3,14]), solver.Word("banana", 10, [1,5,10,15,2])]], board=board)
    elif request.method == 'GET':
        return 'Oops!'



if __name__ == "__main__":
    #app.run(debug=True)
    app.run()
