from flask import Flask, render_template, request, redirect, session
import mysql.connector
import pyrebase
from app_config import *
import os

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

app = Flask(__name__)
app.secret_key = os.urandom(24)


# conn = mysql.connector.connect(host=db_host, user=db_username, password=db_password, database=db_name)
# cur = conn.cursor()


@app.route('/')
def login():
    if 'user_id' in session:
        return redirect('/home')

    else:
        return render_template("login.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/home')
def home():
    if 'user_id' in session:
        print(f"USER  ======> {session['user_id']}")
        try:
            conn = mysql.connector.connect(host=db_host, user=db_username, password=db_password, database=db_name)
            cur = conn.cursor(dictionary=True)
            print("MySQL connected...")
            cur.execute("""SELECT * FROM `tracks`""")
            TRACKS = cur.fetchall()
            print(f"TRACKS : {TRACKS}")
        except:
            print("MySQL connection error !!!.....")
        finally:
            cur.close()
            conn.close()
            print("MySQL disconnected...")
        return render_template("home.html", TRACKS=TRACKS)
    else:
        return redirect('/')

    # try:
    #     conn = mysql.connector.connect(host=db_host, user=db_username, password=db_password, database=db_name)
    #     cur = conn.cursor(dictionary=True)
    #     print("MySQL connected...")
    #     cur.execute("""SELECT * FROM `tracks`""")
    #     TRACKS = cur.fetchall()
    #     print(f"TRACKS : {TRACKS}")
    # except:
    #     print("MySQL connection error !!!.....")
    # finally:
    #     cur.close()
    #     conn.close()
    #     print("MySQL disconnected...")


@app.route('/login_validation', methods=['POST', 'GET'])
def login_validation():
    email = request.form.get('lemail')
    password = request.form.get('lpassword')

    try:
        conn = mysql.connector.connect(host=db_host, user=db_username, password=db_password, database=db_name)
        cur = conn.cursor()
        print("MySQL connected...")
        cur.execute(
            """SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email, password))
        users = cur.fetchall()
        print(users)

        # cur.execute("""SELECT * FROM `tracks`""")
        # mysongs = cur.fetchall()
        # print(mysongs)

    except:
        print("MySQL connection error !!!.....")
    finally:
        cur.close()
        conn.close()
        print("MySQL disconnected...")

    if len(users) > 0:
        session['user_id'] = users[0][0]
        session['first_name'] = users[0][1]
        session['last_name'] = users[0][2]
        session['email'] = users[0][3]
        session['username'] = users[0][4]
        session['gender'] = users[0][5]
        session['dob'] = users[0][6]
        session['country'] = users[0][7]
        session['phone_no'] = users[0][8]
        session['password'] = users[0][9]

        print(session)
        return redirect('/home')
    else:
        return redirect('/')


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    first_name = request.form.get('sfirstname')
    last_name = request.form.get('slastname')
    email = request.form.get('semail')
    gender = request.form.get('sgender')
    dob = request.form.get('sdob')
    country = request.form.get('scountry')
    phone = request.form.get('sphone')
    username = request.form.get('susername')
    password = request.form.get('spassword')

    try:
        conn = mysql.connector.connect(host=db_host, user=db_username, password=db_password, database=db_name)
        cur = conn.cursor()
        print("MySQL connected...")
        cur.execute(
            """INSERT INTO `users` (`user_id`, `first_name`, `last_name`, `email`, `username`, `gender`, `dob`, `country`, `phone_no`, `password`) VALUES (NULL,'{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(
                first_name, last_name, email, username, gender, dob, country, phone, password))
        conn.commit()

        cur.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
        myuser = cur.fetchall()
        print(myuser)
    except:
        print("MySQL connection error !!!.....")
    finally:
        cur.close()
        conn.close()
        print("MySQL disconnected...")

    # session['user_id'] = myuser[0][0]
    # session['first_name'] = myuser[0][1]
    # session['last_name'] = myuser[0][2]
    # session['email'] = myuser[0][3]
    # session['username'] = myuser[0][4]
    # session['gender'] = myuser[0][5]
    # session['dob'] = myuser[0][6]
    # session['country'] = myuser[0][7]
    # session['phone_no'] = myuser[0][8]
    # session['password'] = myuser[0][9]
    # return redirect('/home')
    return redirect('/')


@app.route('/logout')
def logout():
    # session.pop('user_id')
    # session.pop('first_name')
    # session.pop('last_name')
    # session.pop('email')
    # session.pop('username')
    # session.pop('gender')
    # session.pop('dob')
    # session.pop('country')
    # session.pop('phone_no')
    # session.pop('password')
    session.clear()

    return redirect('/')


@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/add_track', methods=['POST', 'GET'])
def add_track():
    if 'user_id' in session:
        return render_template('addTrack.html')
    else:
        return redirect('/')


@app.route('/upload_track', methods=['POST', 'GET'])
def upload_track():
    track_name = request.form.get('atrackname')
    artist = request.form.get('aartist')
    genre = request.form.get('agenre')
    description = request.form.get('adescription')
    upload_aud = request.files['atrackfile']
    upload_img = request.files['aalbum-cover']
    # track_album_cover = request.form.get('aalbum-cover')

    # {session['user_id']}

    no_space_aud = f"{track_name}.mp3".replace(" ", "")
    no_space_img = f"{track_name}.jpg".replace(" ", "")

    path_on_cloud_aud = f"audio/{no_space_aud}"
    path_on_cloud_img = f"image/{no_space_img}"

    storage.child(path_on_cloud_aud).put(upload_aud)
    storage.child(path_on_cloud_img).put(upload_img)

    link_aud = storage.child(path_on_cloud_aud).get_url(None).replace(
        "https://firebasestorage.googleapis.com/v0/b/test-7bd1e.appspot.com/o/audio%2F", "").replace(".mp3?alt=media",
                                                                                                     "")
    link_img = storage.child(path_on_cloud_img).get_url(None).replace(
        "https://firebasestorage.googleapis.com/v0/b/test-7bd1e.appspot.com/o/image%2F", "").replace(".jpg?alt=media",
                                                                                                     "")

    # link_aud.replace("https://firebasestorage.googleapis.com/v0/b/test-7bd1e.appspot.com/o/audio%2F","")
    # link_img.replace("https://firebasestorage.googleapis.com/v0/b/test-7bd1e.appspot.com/o/image%2F","")

    print(link_aud)
    print(link_img)

    try:
        conn = mysql.connector.connect(host=db_host, user=db_username, password=db_password, database=db_name)
        cur = conn.cursor()
        print("MySQL connected...")
        cur.execute(
            f'''INSERT INTO `tracks` (`track_id`, `track_name`,`artist`,`genre`,`description`,`track_link`,`album_link`,`track_user_id`) VALUES (NULL,"{track_name}","{artist}","{genre}","{description}","{link_aud}","{link_img}","{session["user_id"]}")''')
        conn.commit()
        print("inserted")
        cur.execute("""SELECT * FROM `tracks`""")
        TRACKS = cur.fetchall()
        print(TRACKS)
    except:
        print("MySQL connection error !!!.....")
    finally:
        cur.close()
        conn.close()
        print("MySQL disconnected...")

    return redirect('/home')


# @app.context_processor
# def context_processor():
#     try:
#         conn = mysql.connector.connect(host=db_host, user=db_username, password=db_password, database=db_name)
#         cur = conn.cursor(dictionary=True)
#         print("MySQL connected...")
#         cur.execute("""SELECT * FROM `tracks`""")
#         TRACKS = cur.fetchall()
#         print(f"TRACKS : {TRACKS}")
#
#     except:
#         print("MySQL connection error !!!.....")
#     finally:
#         cur.close()
#         conn.close()
#         print("MySQL disconnected...")
#
#     return dict(TRACKS = TRACKS)

@app.route('/playlist', methods=['POST', 'GET'])
def playlist():
    if 'user_id' in session:
        try:
            conn = mysql.connector.connect(host=db_host, user=db_username, password=db_password, database=db_name)
            cur = conn.cursor(dictionary=True)
            print("MySQL connected...")
            # print(f"USER  ======> {session['user_id']}")
            cur.execute(f"""SELECT * FROM `tracks` WHERE `track_user_id` LIKE '{session['user_id']}' """)
            USER_TRACKS = cur.fetchall()
            print(f"TRACKS : {USER_TRACKS}")
        except:
            print("MySQL connection error !!!.....")
        finally:
            cur.close()
            conn.close()
            print("MySQL disconnected...")
        return render_template("playlist.html", USER_TRACKS=USER_TRACKS)
    else:
        return redirect('/')


@app.route('/delete/<string:info>', methods=['POST', 'GET'])
def delete(info):
    words = info.split("|")
    print(info)
    print(words)
    return f"track_id : {words[0]} track_link : {words[1]} album_link : {words[2]}"


if __name__ == "__main__":
    app.run(debug=True)


# test