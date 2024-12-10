from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your app key'

# MySQL Connection
conn = mysql.connector.connect(
  host="your hostname",
  user="username",
  password="password",
  database="db name"
)

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    if cursor.fetchone():
        return render_template('register.html', error='Username already exists')
    cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
    conn.commit()
    session['username'] = username
    return render_template('register.html',succes='Your account is created succefully')
  else:
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
    user = cursor.fetchone()
    if user:
      session['username'] = user[1]
      return redirect('/')
    else:
      return render_template('login.html', error='Invalid username or password')
  else:
    return render_template('login.html')

# Home Route
@app.route('/')
def home():
  if 'username' in session:
    return render_template('home.html', username=session['username'])
  else:
    return redirect('/login')

# Logout Route
@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
