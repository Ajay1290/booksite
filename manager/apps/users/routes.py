from flask import Blueprint, redirect, request, flash, url_for, render_template, current_app
from flask_login import login_required, login_user, current_user, logout_user
from manager.lib.safe_next_url import safe_next_url
from manager.apps.users.decorators import anonymous_required
from manager.models import Users
from manager.apps.users.forms import LoginForm, BeginPasswordResetForm, PasswordResetForm, SignupForm
from manager.apps.users.forms import UpdateCredentials, SendEmailAgainForm
from manager.ext import db
from manager.lib.flask_mailplus import send_email
from manager.models.Books import Books

users = Blueprint('users', __name__)

@users.route('/<username>')
def account(username):
    user = Users.query.filter_by(username=username).first_or_404()
    user.pg_views += 1
    db.session.commit()
    form = UpdateCredentials()
    books = Books.query.filter_by(user=user).filter(Books.post_status == 0) \
            .order_by(Books.created_on.desc()) \
            .paginate(page=request.args.get('page' ,1 ,type=int) ,per_page=10)
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

@users.route('/users/begin_password_reset', methods=['GET', 'POST'])
@anonymous_required()
def begin_password_reset():
    form = BeginPasswordResetForm()
    if form.validate_on_submit():
        print('d')
        u = Users.initialize_password_reset(request.form.get('identity'))
        flash('An email has been sent to {0}.'.format(u.email), 'success')
        return redirect(url_for('users.login'))
    return render_template('apps/users/begin_password_reset.html', form=form)


@users.route('/account/password_reset', methods=['GET', 'POST'])
@anonymous_required()
def password_reset():
    form = PasswordResetForm(reset_token=request.args.get('reset_token'))
    if form.validate_on_submit():
        u = Users.deserialize_token(request.form.get('reset_token'))
        if u is None:
            flash('Your reset token has expired or was tampered with.', 'danger')
            return redirect(url_for('users.begin_password_reset'))
        form.populate_obj(u)
        u.password = Users.encrypt_password(request.form.get('password'))
        u.save()
        if login_user(u):
            flash('Your password has been reset.', 'success')
            return redirect(url_for('users.settings'))
    return render_template('apps/main/before_signup/auth/password_reset.html', form=form)

@users.route('/confirm-email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    data = Users.deserialize_token(token)
    form = SendEmailAgainForm()
    if form.validate_on_submit():
        confirm_url = url_for('users.email_confirmed', token=token, _external=True)
        html = render_template('mails/confirm_email.html', username=data['user_username'],
                                confirm_url=confirm_url)
        send_email(to= data['user_email'], subject= 'Email Confirmation - [ Agust Accounting ]',template= html)
        flash('We have send you email again check this time it may took longer than usual sometime.', 'secondary')
        return redirect(url_for('users.confirm_email', token=token))
    return render_template('apps/main/before_signup/auth/confirm_email.html', form=form, data=data)


@users.route('/email-confirmed/<token>', methods=['GET', 'POST'])
def email_confirmed(token):
    try:
        data = Users.deserialize_token(token)
    except:
        flash('The confirmation link is invalid or has expired, please ask for send again email.', 'danger')
        return redirect(url_for('users.confirm_email'))
    user = Users.find_by_identity(data['user_username'])
    if user:
        flash('Account already confirmed.', 'success')
        login_user(user)
        return redirect(url_for('main.home'))
    else:
        user = Users(username = data['user_username'],
                     email = data['user_email'],
                     phone = data['user_phone'],
                     password = data['user_password'])
        db.session.add(user)
        user.email_confirmed = True
        db.session.commit()
        login_user(user)
        flash('You have confirmed your account. Thank you, for your coopreation.', 'success')
        return redirect(url_for('users.welcome'))
    return redirect(url_for('main.home'))