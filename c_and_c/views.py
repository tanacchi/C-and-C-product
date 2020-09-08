from flask import render_template
from c_and_c import app

@app.route('/')
def root():
    return render_template('index.html')
