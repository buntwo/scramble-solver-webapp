#!/usr/bin/python3

from flask import Flask, render_template, request, jsonify
import solver
import re

app = Flask(__name__)

@app.route('/')
def input():
    return render_template('input.html', lettervals=solver.LETTER_VALS)

@app.route('/view_solutions')
def view_solns():
    line = request.args.get('input', '', type=str)
    sort = request.args.get('sortby', 'scoreD', type=str)
    board, mults = solver.extract_board(line)
    data = { 'board': ''.join(board),
             'mults': mults,
             'lettervals': solver.LETTER_VALS,
             'line': line,
             'sortby': sort,
           }
    return render_template('viewer.html', **data)

@app.route('/solve')
def solve():
    line = request.args.get('line', '', type=str)
    sort = request.args.get('sortby', 'scoreD', type=str)
    words = solver.solve(line, sort)
    data = { 'words': [ x.__dict__ for x in words], }

    return jsonify(data)
    #return render_template('viewer.html', words=[ x.__dict__ for x in [solver.Word("apple", 50, [1,3,14]), solver.Word("banana", 10, [1,5,10,15,2])]], board=''.join(board), mults=['','','','','','','','','','','','','','','','DL'], lettervals=solver.LETTER_VALS)



if __name__ == "__main__":
    app.run(debug=True)
    #app.run('0.0.0.0')
