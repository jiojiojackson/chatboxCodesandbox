import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

conn = sqlite3.connect('chat.db')
cursor = conn.cursor()
# cursor.execute("SELECT password_hash FROM user WHERE id='prominem1'")
# username = 'prominem'
# cursor.execute('SELECT password_hash FROM user WHERE id=?', (username,))
# password_hash = cursor.fetchone()
cursor.execute('SELECT * FROM message')
messages = cursor.fetchall()
conn.close()
# if not password_hash:
#     print('none')
# print(password_hash[0])
# print(check_password_hash(password_hash, 'Yangjisheng'))
print(messages)