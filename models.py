from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """Пользователи. Авторизация и регистрация через БД SQLITE"""
    __bind_key__ = 'sqlite' # убрать при использовании app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'путь к базе'
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Аналог IDENTITY(1,1)
    name = db.Column(db.String(255), nullable=False, unique=True)  # VARCHAR(255) NOT NULL
    psw = db.Column(db.String(255), nullable=False)  # VARCHAR(255) NOT NULL

    def set_password(self, password):
        self.psw = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.psw, password)

    @classmethod
    def create_user(cls, username, password):
        """Создает пользователя с хешированным паролем"""
        user = cls()
        user.name = username
        user.set_password(password)
        return user

    def __repr__(self):
        return f'<User {self.name}>'


# class Data(db_data.Model):
#     """Данные. Обращение к БД MSSQL"""
#     #  __bind_key__ = 'mssql'  # убрать при использовании app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'путь к базе'
#     # __tablename__ = 'UsersTest'
#     # __table_args__ = {'schema': 'dbo'}
#
#     pass
