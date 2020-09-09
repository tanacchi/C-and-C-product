from flask import render_template
from c_and_c import app, db
from c_and_c.models import (
    User, History, Briefing
)
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
    if request.method == 'GET':
        return render_template('history/create.html')
    else:
        user_id = get_current_user()
        current_user = User.query.get(user_id)
        new_history = History()
        new_history.body = request.form.get("body")
        current_user.history.append(new_history)
        db.session.add(new_history)
        db.session.commit()
        print("History created.")

    return redirect(url_for('root'))


@app.route('/history')
def user_history():
    user_id = get_current_user()
    current_user = User.query.get(user_id)
    histories = current_user.history
    return render_template("history/list.html", histories=histories)


@app.route('/briefing/create', methods=['GET', 'POST'])
def create_briefing():
    user_id = get_current_user()
    current_user = User.query.get(user_id)
    if current_user.name == "admin":
        if request.method == 'GET':
            return render_template("briefing/create.html")
        else:
            print("POST briefing")
            briefing = Briefing()
            briefing.description = request.form.get("description")
            db.session.add(briefing)
            db.session.commit()
            briefings = Briefing.query.all()
            return redirect(url_for('list_briefing'))

    print("You are not admin")
    return render_template("index.html")


@app.route('/briefing')
def list_briefing():
    briefings = Briefing.query.all()
    return render_template("briefing/list.html", briefings=briefings)
