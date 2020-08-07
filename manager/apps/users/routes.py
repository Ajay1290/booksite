from flask import Blueprint, redirect, request, flash, url_for, render_template, current_app
from flask_login import login_required, login_user, current_user, logout_user

from manager.lib.safe_next_url import safe_next_url
from manager.apps.users.decorators import anonymous_required
from manager.models import Users
from manager.apps.users.forms import LoginForm, BeginPasswordResetForm, PasswordResetForm, SignupForm
from manager.apps.users.forms import UpdateCredentials
from manager.ext import db
from manager.models.Books import Books

users = Blueprint('users', __name__)

@users.route('/<username>')
def account(username):
    user = Users.query.filter_by(username=username).first_or_404()    
    user.pg_views += 1
    db.session.commit()
    form = UpdateCredentials()
    books = Books.query.filter_by(user=user).filter(Books.post_status == 0).order_by(Books.created_on.desc()).paginate(page=request.args.get('page' ,1 ,type=int) ,per_page=10)
    return render_template('apps/users/account.html',form=form, user=user, books=books)


@users.route('/login', methods=['GET','POST'])
@anonymous_required()
def login():
    form = LoginForm(next=request.args.get('next'))
    if form.validate_on_submit():
        u = Users.find_by_identity(form.identity.data)
        if u and u.authenticated(password=form.password.data):
            is_remembered = request.form.get('remember', False)
            login_user(u, remember=is_remembered)
            u.is_active(True)
            u.update_activity_tracking(request.remote_addr)
            next_url = request.form.get('next')
            if next_url:
                return redirect(safe_next_url(next_url))
            return redirect(url_for('main.home'))
        else:
            flash('Identity or password is incorrect.', 'danger')
    return render_template('apps/users/login.html', form=form)


@users.route('/register', methods=['GET','POST'])
@anonymous_required()
def register():
    form = SignupForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data.lower(),
                     password = form.password.data,
                     email=form.email.data.lower())
        db.session.add(user)
        db.session.commit()
        if login_user(user):
            user.update_activity_tracking(request.remote_addr)
            flash('Welcome, and browse books of your need.', 'success')
            return redirect(url_for('main.home'))
    return render_template('apps/users/register.html', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/reset-password')
def reset_password():
    return render_template('apps/users/reset_password.html')


@users.route('/email_confirmation')
def email_confirmation():
    return render_template('apps/users/email_confirmation.html')    