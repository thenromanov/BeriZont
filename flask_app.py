from flask import Flask, render_template, redirect, request, make_response, jsonify, url_for
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from wtforms import IntegerField, StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, length
from secrets import token_urlsafe
from data import dbSession
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = token_urlsafe(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/berizont.db'

loginManager = LoginManager()
loginManager.init_app(app)


class RegisterForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    passwordRepeat = PasswordField('Повтор пароля', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@loginManager.user_loader
def loadUser(id):
    session = dbSession.createSession()
    return session.query(User).get(id)


@app.route('/', methods=['GET', 'POST'])
def primary():
    return render_template('main.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.passwordRepeat.data:
            return render_template('register.html', title='Регистрация', form=form, message='Пароли не совпадают')
        session = dbSession.createSession()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form, message='Пользователь уже существует')
        user = User(email=form.email.data,
                    surname=form.surname.data,
                    name=form.name.data)
        user.setPassword(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = dbSession.createSession()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.checkPassword(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect('/')
        return render_template('login.html', title='Вход', form=form, message='Неверный логин или пароль')
    return render_template('login.html', title='Вход', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


def main():
    dbSession.globalInit('db/berizont.db')
    app.run()


if __name__ == '__main__':
    main()
