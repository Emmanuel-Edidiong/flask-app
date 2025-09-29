from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            session.permanent = True
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Please enter a username', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """User logout."""
    username = session.get('username')
    session.pop('username', None)
    if username:
        flash(f'Goodbye, {username}!', 'info')
    return redirect(url_for('main.home'))

@auth_bp.route('/profile')
def profile():
    """User profile page."""
    if 'username' not in session:
        flash('Please log in to view your profile', 'warning')
        return redirect(url_for('auth.login'))
    
    user_data = {
        'username': session.get('username'),
    }
    return render_template('auth/profile.html', user=user_data)
