from flask import Blueprint, render_template, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Home page with navigation to different features."""
    user_data = None
    if 'username' in session:
        user_data = {
            'username': session.get('username')
        }
    
    return render_template('index.html', user=user_data)

@main_bp.route('/about')
def about():
    """About page describing the interior design tool."""
    return render_template('about.html')
