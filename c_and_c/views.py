from flask import render_template
from c_and_c import app, db
from c_and_c.models import User
from c_and_c.utils import (
    session_login, is_logged_in,
    get_current_user, session_logout
)
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('users/login.html')
    else:
        user_name = request.form.get("name")
        user = User.query.filter_by(name=user_name).first()
        if user:
            session_login(user.id)
            print(f"logged in as {user_name}")
        else:
            print("login failed.")
    return redirect(url_for('root'))


@app.route('/history/create', methods=['GET', 'POST'])
def create_history():
    print(f"{request.method}")
    return redirect(url_for('root'))
