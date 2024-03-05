from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user


auth = Blueprint('auth', __name__)


##################################################################LOGIN##################################################################
@auth.route('/login')
def login():
    return render_template('login.html')



@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    #проверка наличия юзера, хеш введенного пароля и сравнение с паролем в бд
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) #не сущ. юзер или ошибка пароля => релод страницы

    # все норм => на лк
    login_user(user, remember = remember) ##оштбка, проверить будет ли сохранена сессия
    return redirect(url_for('main.profile'))
##################################################################LOGIN##################################################################





##################################################################SIGNUP##################################################################
@auth.route('/signup')
def signup():
    return render_template('signup.html')



@auth.route('/signup', methods=['POST'])
def signup_post(): #проверка и добавление пользователя в бд

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email = email).first()  #возврат юзера => существует

    if user:  #юзер найден => на регу снова
        flash('почта уже зарегистрирована') #вывод сообщения на экран (см. signup.html)
        return redirect(url_for('auth.signup'))

    #создание нового и хэш его пароля
    new_user = User(email = email, name = name, password = generate_password_hash(password, method='pbkdf2'))

    #добавления юзер в бд
    db.session.add(new_user)
    db.session.commit()


    return redirect(url_for('auth.login'))
##################################################################SIGNUP##################################################################





##################################################################LOGOUT##################################################################
@auth.route('/logout')
def logout():
    return 'Logout'
##################################################################LOGOUT##################################################################