"""Управление SQLite БД. Функции"""
from sqlite_manager import SQLiteManager
from UserLogin import User
from werkzeug.security import generate_password_hash


def demo_crud_operations():
    """Раскомментируем то, что нужно для выполнения запроса/транзакции"""

    # Инициализация
    db = SQLiteManager('../users.db')

    try:
        # # Создание таблицы
        # columns = {
        #     'user_id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        #     'name': 'TEXT NOT NULL',
        #     'psw': 'TEXT UNIQUE',
        # }
        # db.create_table('users', columns)
        #
        # # Добавление записей
        # user_id = db.insert_record('users', {
        #     'name': 'vasya',
        #     'psw': f'({generate_password_hash("Abcd1234")})',
        # })
        # print(f"Пользователь добавлен")
        #
        # # Получение одной записи
        # user = db.get_record_by_id('users', None)
        # print(f"Пользователь с ID:", user)
        #
        # # Обновление пароля
        # success = db.update_record('users', 12, {"psw": f'({generate_password_hash("Abcd1234")})'})
        # print(f"Обновление пользователя: {'Успешно' if success else 'Не удалось'}")
        #
        # # Удаление записей
        # for i in range(100):
        #     success = db.delete_record('users', i)
        #     print(f"Удаление пользователя: {'Успешно' if success else 'Не удалось'}")
        #
        # # Удаление одной записи
        # user_id = None
        # success = db.delete_record('users', user_id)
        # print(f"Удаление пользователя с id {user_id}: {'Успешно' if success else 'Не удалось'}")
        #
        # # Фильтрация
        # user_name = db.get_all_records('users', 'name = ?', ('admin',))
        # print("Пользователь ", user_name)

        # Получение всех записей
        all_users = db.get_all_records('users')
        print("Все пользователи:")
        for user in all_users:
            print(user)
        # Подсчет записей
        count = db.count_records('users')
        print(f"Всего пользователей: {count}")

    finally:
        db.close()


if __name__ == "__main__":
    demo_crud_operations()
