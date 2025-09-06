"""Авторизация. Соединение с базой. Маршруты."""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from dotenv import load_dotenv
import os
from extensions import db, login_manager
from forms import LoginForm, RegForm


load_dotenv()   # Чтение параметров из .env файла

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['DEBUG'] = True

# Конфигурация MSSQL, сквозная авторизация в БД, в случае авторизации через MSSQL-таблицу пользователей использовать:
# f"mssql+pyodbc://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
# f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?driver=ODBC+Driver+17+for+SQL+Server"
app.config['SQLALCHEMY_BINDS'] = {
    'mssql': (
        f"mssql+pyodbc://{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?"
        "trusted_connection=yes&"
        "driver=ODBC+Driver+17+for+SQL+Server"
    ),
    'sqlite': f"sqlite:///{os.path.join(app.root_path, 'users.db')}"
}
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.root_path, 'users.db')}" # если уберем MSSQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Инициализация расширений
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


# Импорт после инициализации!
from models import User
from UserLogin import UserLogin


@login_manager.user_loader
def load_user(user_id):
    """Создаёт право на просмотр только залогиненым юзерам"""
    return UserLogin().fromDB(user_id)


@app.route("/")
@login_required
def index():
    """Главная"""
    return render_template('index.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    """Авторизация"""
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST' and form.validate():
        name = form.name.data
        psw = form.psw.data
        user = User.query.filter_by(name=name).first()
        if user and user.check_password(psw): # and user.psw == psw
            user_login = UserLogin().create(user)
            login_user(user_login, remember=True)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Неверный логин/пароль!', 'error')
    return render_template("auth.html", form=form)


@app.route("/register", methods=['POST', 'GET'])
def register():
    """Регистрация"""
    form = RegForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST' and form.validate():
        name = form.name.data
        psw = form.psw.data
        # Проверяем, нет ли такого пользователя
        if User.query.filter_by(name=name).first():
            flash('Пользователь с таким именем уже существует!', 'error')
        else:
            # Создаем нового пользователя
            try:
                new_user = User().create_user(name, psw)
                db.session.add(new_user)
                db.session.commit()
                flash('Регистрация успешна! Теперь можно войти.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при регистрации: ' + str(e), 'error')
    return render_template("reg.html", form=form)


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    """Выход из профиля"""
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run()
