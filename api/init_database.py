import sqlite3
from werkzeug.security import generate_password_hash
from models import *

conn = sqlite3.connect('chat.db')
with open('schema.sql', 'r') as f:
    schema = f.read()
conn.executescript(schema)
conn.close

# 初始化用户名和密码
user1 = 'prominem'
passwd1 = 'Yangjisheng'
password_hash = generate_password_hash(passwd1)
add_user(user1, password_hash)
user2 = 'elaine'
passwd2 = 'wayjs'
password_hash = generate_password_hash(passwd2)
add_user(user2, password_hash)

