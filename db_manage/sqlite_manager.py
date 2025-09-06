"""Управление SQLite БД users"""

import sqlite3
# import os
from typing import List, Dict, Any, Optional


class SQLiteManager:
    def __init__(self, db_path: str = None):
        """
        Инициализация менеджера БД

        :param db_path: Путь к файлу БД. Если None, использует database.db в текущей директории
        """
        self.db_path = db_path # or os.path.join(os.path.dirname(__file__), 'users.db')
        self.connection = None

    def connect(self) -> sqlite3.Connection:
        """Устанавливает соединение с БД"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Для получения результатов в виде словаря
        return self.connection

    def close(self):
        """Закрывает соединение с БД"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query: str, params: tuple = None) -> sqlite3.Cursor:
        """
        Выполняет SQL-запрос

        :param query: SQL-запрос
        :param params: Параметры для запроса
        :return: Курсор с результатами
        """
        if not self.connection:
            self.connect()

        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Ошибка выполнения запроса: {e}")
            if self.connection:
                self.connection.rollback()
            raise

    # CRUD операции
    def create_table(self, table_name: str, columns: Dict[str, str]):
        """
        Создает таблицу

        :param table_name: Имя таблицы
        :param columns: Словарь {имя_колонки: тип_данных}
        """
        columns_def = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"
        self.execute_query(query)
        print(f"Таблица {table_name} создана/проверена")

    def insert_record(self, table_name: str, data: Dict[str, Any]) -> int:
        """
        Добавляет запись в таблицу

        :param table_name: Имя таблицы
        :param data: Словарь {колонка: значение}
        :return: ID добавленной записи
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = tuple(data.values())

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor = self.execute_query(query, values)
        return cursor.lastrowid

    def get_all_records(self, table_name: str, where: str = None, params: tuple = None) -> List[Dict]:
        """
        Получает все записи из таблицы

        :param table_name: Имя таблицы
        :param where: Условие WHERE (опционально)
        :param params: Параметры для условия--
        :return: Список словарей с записями
        """
        query = f"SELECT * FROM {table_name}"
        if where:
            query += f" WHERE {where}"

        cursor = self.execute_query(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_record_by_id(self, table_name: str, record_id: int) -> Optional[Dict]:
        """
        Получает запись по ID

        :param table_name: Имя таблицы
        :param record_id: ID записи
        :return: Словарь с данными записи или None
        """
        query = f"SELECT * FROM {table_name} WHERE user_id = ?"
        cursor = self.execute_query(query, (record_id,))
        result = cursor.fetchone()
        return dict(result) if result else None

    def update_record(self, table_name: str, record_id: int, data: Dict[str, Any]) -> bool:
        """
        Обновляет запись

        :param table_name: Имя таблицы
        :param record_id: ID записи
        :param data: Словарь {колонка: новое_значение}
        :return: True если успешно, False если запись не найдена
        """
        set_clause = ', '.join([f"{col} = ?" for col in data.keys()])
        values = tuple(data.values()) + (record_id,)

        query = f"UPDATE {table_name} SET {set_clause} WHERE user_id = ?"
        cursor = self.execute_query(query, values)
        return cursor.rowcount > 0

    def delete_record(self, table_name: str, record_id: int) -> bool:
        """
        Удаляет запись

        :param table_name: Имя таблицы
        :param record_id: ID записи
        :return: True если успешно, False если запись не найдена
        """
        query = f"DELETE FROM {table_name} WHERE user_id = ?"
        cursor = self.execute_query(query, (record_id,))
        return cursor.rowcount > 0

    def count_records(self, table_name: str, where: str = None, params: tuple = None) -> int:
        """
        Считает количество записей

        :param table_name: Имя таблицы
        :param where: Условие WHERE (опционально)
        :param params: Параметры для условия
        :return: Количество записей
        """
        query = f"SELECT COUNT(*) FROM {table_name}"
        if where:
            query += f" WHERE {where}"

        cursor = self.execute_query(query, params)
        return cursor.fetchone()[0]

    def table_exists(self, table_name: str) -> bool:
        """
        Проверяет существование таблицы

        :param table_name: Имя таблицы
        :return: True если таблица существует
        """
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        cursor = self.execute_query(query, (table_name,))
        return cursor.fetchone() is not None

    # Контекстный менеджер для with
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
