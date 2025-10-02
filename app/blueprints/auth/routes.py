from flask import render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from . import bp
from .forms import LoginForm, RegisterForm
from ...extensions import db, login_manager
from ...models.user import User
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
@bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('org.dashboard'))
        flash('Invalid email or password','danger')
    return render_template('auth/login.html', form=form)
@bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash('Email already registered','warning')
        else:
            u = User(name=form.name.data, email=form.email.data.lower(), password_hash=generate_password_hash(form.password.data), role='Assessor')
            db.session.add(u); db.session.commit()
            flash('Account created. Please log in.','success')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
