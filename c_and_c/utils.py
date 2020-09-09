from flask import session

login_key = 'user_id'

def session_login(id):
    print(f"Logged in as id: {id}")
    session[login_key] = id


def is_logged_in():
    return login_key in session


def get_current_user():
    return session.get(login_key)


def session_logout():
    session[login_key] = None
