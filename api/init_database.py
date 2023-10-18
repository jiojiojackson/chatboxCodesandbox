import sqlite3
from werkzeug.security import generate_password_hash
from index import *
import os

current_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(current_path)
tmp_dir = os.path.join(root_path, 'tmp')
if not os.path.exists(tmp_dir): os.mkdir(tmp_dir)
data_dir = os.path.join(tmp_dir, 'chat.db')

conn = sqlite3.connect(data_dir)
with open(os.path.join(current_path, 'schema.sql'), 'r') as f:
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

