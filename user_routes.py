from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Category, db, User

user_bp = Blueprint('user_routes', __name__, url_prefix='/user')

@user_bp.route('/user-panel')
@login_required
def user_panel():
    categories = Category.query.all() 
    user_data = {
        "username": current_user.username,
        "email": current_user.email
    }

    return render_template('user_panel.html', user=user_data)

@user_bp.route('/update-user', methods=['POST'])
@login_required  
def update_user():
    username = request.form.get('username')
    email = request.form.get('email')

    if username != "" or email != "":
        if username and username != current_user.username:
            current_user.username = username
            db.session.commit()
            flash('Dane użytkownika zostały zaktualizowane!', 'success')

        if email and email != current_user.email:
            current_user.email = email
            db.session.commit()
            flash('Dane użytkownika zostały zaktualizowane!', 'success')
    else:
        flash('Musisz podac jakies dane do zmiany!', 'danger')

    return redirect(url_for('user_routes.user_panel'))

@user_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not check_password_hash(current_user.password, current_password):
        flash('Bieżące hasło jest nieprawidłowe', 'danger')
        return redirect(url_for('user_routes.user_panel'))

    if new_password != confirm_password:
        flash('Nowe hasło i potwierdzenie hasła nie są zgodne', 'danger')
        return redirect(url_for('user_routes.user_panel'))

    current_user.password = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=16)
    db.session.commit()

    flash('Hasło zostało zmienione!', 'success')
    return redirect(url_for('user_routes.user_panel'))