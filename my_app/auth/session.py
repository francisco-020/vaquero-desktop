# my_app/auth/session.py
current_user_id = None

def set_user_id(uid):
    global current_user_id
    current_user_id = uid

def get_user_id():
    return current_user_id
