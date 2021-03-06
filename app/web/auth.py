from flask import render_template, request, redirect, url_for, flash
from app.forms.auth import RegisterForm, LoginForm, EmailForm, RestPasswordForm
from app.libs.email import send_email
from app.models.base import db
from app.models.user import User
from . import web
from flask_login import login_user, logout_user

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或者密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            email_data = form.email.data
            user = User.query.filter_by(email=email_data).first_or_404()
            # send_email(1, 1, 1)
            send_email(form.email.data, '重置你的密码',
                       'email/reset_password.html',
                       user=user, token=user.generate_token())
            flash('一封邮件已经发送至你的邮箱'+email_data+'，请及时查收')
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = RestPasswordForm(request.form)
    if form.validate() and request.method == 'POST':
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('你的密码已更新，请重新登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html')



@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    return 'change password'


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
