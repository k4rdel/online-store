from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_login import login_required, current_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/user-panel')
@login_required
def user_panel(): 
    user_data = {
        "username": current_user.username,
        "email": current_user.email,
        "password": current_user.password
    }

    return render_template('user_panel.html', user=user_data)

@user_bp.route('/update-user', methods=['POST'])
@login_required
def update_user():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')

    return redirect(url_for('user.user_panel'))