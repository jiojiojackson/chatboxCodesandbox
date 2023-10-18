from flask import url_for, render_template, request, redirect, flash, Flask, jsonify, send_from_directory
from flask_login import login_user, login_required, LoginManager, UserMixin
import uuid
import datetime
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'lfaldfh4792fdH'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=2)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

img_num = 100

current_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(current_path)
tmp_dir = os.path.join(root_path, 'tmp')
if not os.path.exists(tmp_dir): os.mkdir(tmp_dir)
img_path = os.path.join(tmp_dir, 'images')
if not os.path.exists(img_path): os.mkdir(img_path)

data_dir = os.path.join(tmp_dir, 'chat.db')

class User(UserMixin):
    def __init__(self, name):
        self.id = name
    def get_id(self):
        return str(self.id)

def delete_oldest_images(path, num_to_keep):
    files = os.listdir(path)
    file_dict = {}
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            file_dict[file_path] = os.path.getctime(file_path)
    
    sorted_files = sorted(file_dict.items(), key=lambda x: x[1])
    num_files = len(sorted_files)
    if num_files > num_to_keep:
        files_to_delete = sorted_files[:num_files - num_to_keep]
        for file, _ in files_to_delete:
            os.remove(file)
            print(f"Deleted file: {file}")

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


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_login(username, password):
            user = User(username)
            login_user(user)
            if username=='prominem':
                return redirect(url_for('prominem'))
            elif username == 'elaine':
                return redirect(url_for('elaine'))

        flash('用户名或密码错误')
    return render_template('login.html')

@app.route('/get_image/<path:random_uuid>')
def get_image(random_uuid):
    return send_from_directory(img_path, random_uuid+'.jpg')

@app.route('/elaine', methods=['GET', 'POST'])
@login_required
def elaine():
    if request.method == 'POST':
        text = request.form.get('text')
        image = request.files.get('image')
        if image and text:
            random_uuid = str(uuid.uuid4())
            img_dir = os.path.join(img_path, f'{random_uuid}.jpg')
            image.save(img_dir)
            dataUrl = url_for('get_image', random_uuid=random_uuid)
            add_message('elaine', text=text, imgUrl=dataUrl)
        elif image:
            random_uuid = str(uuid.uuid4())
            img_dir = os.path.join(img_path, f'{random_uuid}.jpg')
            image.save(img_dir)
            dataUrl = url_for('get_image', random_uuid=random_uuid)
            add_message('elaine', imgUrl=dataUrl)
        elif text:
            add_message('elaine', text=text)
        else:
            return redirect(url_for('elaine'))
        delete_oldest_images(img_path, img_num)
        return 'yes'
    return render_template('elaine.html')

@app.route('/prominem', methods=['GET', 'POST'])
@login_required
def prominem():
    if request.method == 'POST':
        text = request.form.get('text')
        image = request.files.get('image')
        if image and text:
            random_uuid = str(uuid.uuid4())
            img_dir = os.path.join(img_path, f'{random_uuid}.jpg')
            image.save(img_dir)
            dataUrl = url_for('get_image', random_uuid=random_uuid)
            add_message('prominem', text=text, imgUrl=dataUrl)
        elif image:
            random_uuid = str(uuid.uuid4())
            img_dir = os.path.join(img_path, f'{random_uuid}.jpg')
            image.save(img_dir)
            dataUrl = url_for('get_image', random_uuid=random_uuid)
            add_message('prominem', imgUrl=dataUrl)
        elif text:
            add_message('prominem', text=text)
        else:
            return redirect(url_for('prominem'))
        delete_oldest_images(img_path, img_num)
        return 'yes'
    return render_template('prominem.html')

@app.route('/messages', methods=['GET'])
@login_required
def messages():
    results = get_latest_messages()
    return jsonify(results)

@app.route('/allmessages', methods=['GET'])
@login_required
def allmessages():
    messages = get_messages()
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

