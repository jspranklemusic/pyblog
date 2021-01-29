from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import traceback
import sys

app = Flask(__name__)
app.secret_key="my-secret-key"

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn



@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    if 'user' in session:
        posts = cur.execute('SELECT * FROM posts WHERE user = (?)',(session['user'],)).fetchall()
        posts.reverse()
    else:
        posts = []
    return render_template('index.html', posts=posts)



@app.route('/page1')
def page1():
    return render_template('page1.html')


@app.route('/page2')
def page2():
    return render_template('page2.html')


@app.route('/page3')
def page3():
    return render_template('page3.html')

@app.route('/login',methods=('GET','POST'))
def login():
    if(request.method=='GET'):
        return render_template('login.html')
    else:
        try:

            conn = get_db_connection()

            #checks to see if you are logged in
            is_login_valid = conn.cursor().execute("""
            SELECT * FROM users
            WHERE username = (?)
            AND password = (?)
            """,(request.form['username'],request.form['password'],)).fetchone()
            conn.close()

            # returns you to the page if login is invalid
            if not is_login_valid:
                return render_template('login.html',error="Invalid Login")
            else:
                session['user']=request.form['username']
                return render_template('index.html')
        except sqlite3.Error as err:
            print(err)
            return render_template('login.html',error="Invalid Login")
        


@app.route('/account',methods=('GET','POST'))
def account():
    if(request.method=='GET'):
        return render_template('account.html')
    else:
        print(request.form)
        try:
            conn = get_db_connection()

            #checks if a user exists
            checkuser = conn.cursor().execute("""
                SELECT * FROM users WHERE username = (?)
            """,(request.form['username'],)).fetchone()
            print(checkuser)
            if checkuser:
                return render_template('account.html',error='Username is already taken.')

            #if not, then it will save the user
            conn.execute("""
            INSERT INTO users(username,email,password)
            VALUES (?,?,?)
            """,(request.form['username'],request.form['email'],request.form['password']))
            session['user']=request.form['username']
            conn.commit()
            conn.close()
            return render_template('index.html')
        except sqlite3.Error as err:
            return render_template('account.html',error='SQLite error: %s' % (' '.join(err.args)))

@app.route('/accounts')
def accounts():
    conn = get_db_connection()
    conn.execute("""
    INSERT INTO users(username,email,password)
    VALUES (?,?,?)
    """,(request.form['username'],request.form['email'],request.form['password']))



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/posts',methods=('POST','DELETE','PUT'))
def posts():

    if request.method=='POST':
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO posts (title,content,user)
            VALUES(?,?,?)
        """,(request.form['title'],request.form['content'],session['user']))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))


    elif request.method=='DELETE':
        conn = get_db_connection()
        conn.execute("""
           DELETE FROM posts WHERE id IN (?)
        """,(request.get_json()['id']))
        conn.commit()
        conn.close()
        return('Post successfully deleted!')


    else:
        payload = request.get_json()
        conn = get_db_connection()
        conn.execute("""
           UPDATE posts 
           SET content = (?) 
           WHERE id IN (?)
        """,(payload['content'],payload['id']))
        conn.commit()
        conn.close()
        return('Post successfully updated!')



if __name__=='__main__':
    app.run(debug=True)