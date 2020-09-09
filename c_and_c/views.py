from flask import render_template
from c_and_c import app
from flask import (
    render_template, request,
    abort, redirect, url_for,
    flash
)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('users/create.html')
    else:
        print("User creation.")
        return render_template('index.html')
