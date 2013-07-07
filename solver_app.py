#!/usr/bin/python3

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def view():
    return render_template('layout.html', foo = {'apple': 3})


if __name__ == "__main__":
    app.run(debug=True)
