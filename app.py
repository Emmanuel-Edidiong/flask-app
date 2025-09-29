from flask import Flask, jsonify, request, redirect, url_for, render_template, session

app = Flask(__name__)
app.secret_key = 'a28e847d5329359b41b1b1819556cd1804ab0b5b4d8ef314668b6573ed3b4944'

@app.route('/')
def home():
    list_items = ['joe', 'mary', 'jane', 'david', 'sarah', 'paul', 'linda', 'james', 'laura', 'mike']
    return render_template('index.html', content="John", list_items=list_items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('user'))
    else:
        return render_template('login.html')

@app.route('/user')
def user():
    if 'username' not in session:
        return redirect(url_for('login'))
    userData = {
        'username': session.get('username'),
    }
    return render_template('user-profile.html', user=userData)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# @app.route('/user/<username>')
# def user_profile(username):
#     return render_template('user-profile.html', username=username)

# @app.route('/admin')
# def admin_dashboard():
#     return redirect(url_for('home'))

# @app.route('/admin/user')
# def admin_user():
#     return redirect(url_for('user_profile', username='admin'))

if __name__ == '__main__':
    app.run(debug=True)