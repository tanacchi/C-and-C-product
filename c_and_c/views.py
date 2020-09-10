from flask import render_template
from c_and_c import app, db
from c_and_c.models import (
    User, History, Briefing,
    Lecture
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


NUMBER_USERTYPE_MAP = {
    1: "学生", 2: "企業"
}

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
        new_user.type = int(request.form.get("type"))
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(name=new_user.name).first()
        session_login(user.id)
        return redirect(url_for('root'))


@app.route('/users')
def users_list():
    users = User.query.all()
    name_usertype_list = [(user.name, NUMBER_USERTYPE_MAP[user.type]) for user in users]
    return render_template('users/users.html', data=name_usertype_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('users/login.html')
    else:
        user_name = request.form.get("name")
        user = User.query.filter_by(name=user_name).first()
        if user:
            session_login(user.id)
        else:
            print("login failed.")
            return render_template('users/login.html')
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

    return redirect(url_for('user_history'))


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
            briefing = Briefing()
            briefing.description = request.form.get("description")
            db.session.add(briefing)
            db.session.commit()
            return redirect(url_for('list_briefing'))

    print("You are not admin")
    return redirect(url_for('root'))


@app.route('/briefing')
def list_briefing():
    briefings = Briefing.query.all()
    return render_template("briefing/list.html", briefings=briefings)


@app.route('/briefing/<int:briefing_id>')
def briefing_detail(briefing_id):
    briefing = Briefing.query.get(briefing_id)
    return render_template("briefing/show.html", briefing=briefing)


@app.route('/lectures/create', methods=['GET', 'POST'])
def create_lecture():
    user_id = get_current_user()
    current_user = User.query.get(user_id)
    if current_user.name == "admin":
        if request.method == 'GET':
            return render_template("lectures/create.html")
        else:
            lecture = Lecture()
            lecture.description = request.form.get("description")
            db.session.add(lecture)
            db.session.commit()
            lectures = Lecture.query.all()
            return redirect(url_for('list_lectures'))

    print("You are not admin")
    return redirect(url_for('root'))


@app.route('/lectures')
def list_lectures():
    lectures = Lecture.query.all()
    return render_template("lectures/list.html", lectures=lectures)

@app.route('/entertop')
def enter_top():
    return render_template("users/enter_top.html")
