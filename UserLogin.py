from flask_login import UserMixin
from models import User


class UserLogin(UserMixin):
    """Сессия пользователя с SQLAlchemy"""

    def fromDB(self, user_id):
        """Идентифицирует пользователя в БД"""
        self.__user = User.query.get(int(user_id))
        return self

    def create(self, user):
        """Создаёт пользователя текущей сессии"""
        self.__user = user
        return self

    def get_id(self):
        """Возвращает id пользователя"""
        return str(self.__user.user_id) if self.__user else None

    def getName(self):
        """Возвращает имя пользователя"""
        return self.__user.name if self.__user else "Без имени"

    # def getEmail(self):
    #     """Возвращает e-mail пользователя"""
    #     return self.__user.email if self.__user else "Без e-mail"
