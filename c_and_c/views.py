from flask import render_template
from c_and_c import app, db
from c_and_c.models import User
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
        new_user = User()
        new_user.name = request.form.get("name")
        new_user.type = request.form.get("type")
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('users_list'))


@app.route('/users')
def users_list():
    users = User.query.all()
    return render_template('users/users.html', users=users)
