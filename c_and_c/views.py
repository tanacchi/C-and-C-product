from flask import render_template
from c_and_c import app, db
from c_and_c.models import (
    User, History, Briefing,
    Lecture, UserCompanyTable,
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

STUDENT = 1
COMPANY = 2
NUMBER_USERTYPE_MAP = {
    STUDENT: "学生", COMPANY: "企業"
}
STUDENT_TOPICS = [
    "ハッカソン", "競技プログラミング",
]

@app.route('/')
def root():
    user_id = get_current_user()
    if not user_id:
        return render_template('index.html', is_logged_in=False)
    current_user = User.query.get(user_id)
    if current_user.type == STUDENT:
        return render_template('index.html', is_logged_in=True)
    else:
        students = User.query.filter_by(type=STUDENT)
        return render_template("users/enter_top.html", students=students)


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
            return redirect(url_for('root'))
        else:
            print("login failed.")
            return render_template('users/login.html')


@app.route('/logout')
def logout():
    session_logout()
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
        histories = History.query.filter_by(user_id=user_id)
        student_topics = []
        for history in histories:
            for topic in STUDENT_TOPICS:
                if topic in history.body:
                    student_topics.append(topic)
        student_topics = list(set(student_topics))
        topic_str = ""
        for topic in student_topics:
            topic_str += topic + ", "
        current_user.topic = topic_str
        db.session.add(current_user)
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
            companies = User.query.filter_by(type=COMPANY)
            return render_template("briefing/create.html", companies=companies)
        else:
            briefing = Briefing()
            briefing.description = request.form.get("description")
            participants = request.form.get("participants")
            for attr, value in request.form.items():
                if 'participants' in attr:
                    company_id = attr.split('_')[1]
                    print(company_id, value)
                    company = User.query.get(company_id)
                    briefing.participants.append(company)
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
    user_id = get_current_user()
    current_user = User.query.get(user_id)
    briefing = Briefing.query.get(briefing_id)
    if current_user.type == STUDENT:
        for company in briefing.participants:
            relation = UserCompanyTable.query.filter_by(student_id=user_id, company_id=company.id).first()
            if relation:
                relation.access_count += 1
            else:
                relation = UserCompanyTable()
                relation.student_id = user_id
                relation.company_id = company.id
                relation.access_count = 1
            db.session.add(relation)
            db.session.commit()
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
            return redirect(url_for('list_lectures'))

    print("You are not admin")
    return redirect(url_for('root'))


@app.route('/lectures')
def list_lectures():
    lectures = Lecture.query.all()
    return render_template("lectures/list.html", lectures=lectures)


@app.route('/about')
def about_us():
    return render_template("aboutus.html")


@app.route('/entertop')
def enter_top():
    return render_template("users/enter_top.html")


@app.route('/enterdetails/<int:user_id>')
def student_detail(user_id):
    company_id = get_current_user()
    student = User.query.get(user_id)
    relation = UserCompanyTable.query.filter_by(student_id=user_id, company_id=company_id).first()
    access_count = relation.access_count if relation else 0
    return render_template("users/details.html", student=student, access_count=access_count)


@app.route('/students')
def list_students():
    user_id = get_current_user()
    current_user = User.query.get(user_id)
    if not current_user.type == COMPANY:
        print("You are not company.")
        return redirect(url_for('root'))
    companies = { company.id: company.name for company in User.query.filter_by(type=COMPANY)}
    print(companies)
    students = User.query.filter_by(type=STUDENT)
    students_data = {}
    for student in students:
        access_counts = {}
        for company_id, company_name in companies.items():
            relation = UserCompanyTable.query.filter_by(student_id=student.id, company_id=company_id).first()
            access_counts[company_name] = relation.access_count if relation else 0
        students_data[student.id] = (student.name, access_counts)
    return render_template("users/students.html", students_data=students_data)
