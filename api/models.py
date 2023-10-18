import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime
import os
current_path = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_path, 'chat.db')

class User(UserMixin):
    def __init__(self, name):
        self.id = name
    def get_id(self):
        return str(self.id)

def add_user(id, passwd_hash):
    conn = sqlite3.connect(data_dir)
    cursor = conn.cursor()
    data = (id, passwd_hash)
    cursor.execute('INSERT INTO user (id, password_hash) VALUES (?, ?)', data)
    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()

def check_login(username, passwd):
    conn = sqlite3.connect(data_dir)
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM user WHERE id=?', (username,))
    password_hash = cursor.fetchone()
    conn.close()
    if not password_hash:
        return False
    return check_password_hash(password_hash[0], passwd)

def get_messages():
    conn = sqlite3.connect(data_dir)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM message')
    messages = cursor.fetchall()
    conn.close()
    new_massages = []
    for mess in messages:
        new_massages.append({'id':mess[0], 'name':mess[1], 'text':mess[2], 'imgUrl':mess[3], 'time':mess[4]})
    return new_massages

def add_message(username, text=None, imgUrl=None):
    conn = sqlite3.connect(data_dir)
    cursor = conn.cursor()
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    if text and imgUrl:
        data = (username, text, imgUrl, current_time)
        cursor.execute('INSERT INTO message (username, mytext, imgUrl, mytime) VALUES (?, ?, ?, ?)', data)
    elif text:
        data = (username, text, current_time)
        cursor.execute('INSERT INTO message (username, mytext, mytime) VALUES (?, ?, ?)', data)
    elif imgUrl:
        data = (username, imgUrl, current_time)
        cursor.execute('INSERT INTO message (username, imgUrl, mytime) VALUES (?, ?, ?)', data)
    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()

def get_latest_messages(num=7):
    conn = sqlite3.connect(data_dir)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM message ORDER BY mytime DESC LIMIT {num}")
    results = cursor.fetchall()
    results.reverse()
    new_massages = []
    for mess in results:
        new_massages.append({'id':mess[0], 'name':mess[1], 'text':mess[2], 'imgUrl':mess[3], 'time':mess[4]})
    return new_massages
