#!/usr/bin/python
from flask import Flask, render_template, request, jsonify, send_from_directory
import solver
import re
import os

app = Flask(__name__)

@app.route('/')
def input():
    return render_template('input.html', lettervals=solver.LETTER_VALS)


@app.route('/view_solutions')
def view_solns():
    line = request.args.get('input', '', type=str)
    sort = request.args.get('sortby', 'scoreD', type=str)
    # validate
    if sort not in solver.SORT_ORDERS:
        sort = 'scoreD'
    if not solver.valid(line):
        return render_template('badinput.html')

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


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(debug=True)
    #app.run()
