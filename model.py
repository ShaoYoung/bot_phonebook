# Работа с БД

import sqlite3

# глобальные переменные
db = None
cursor = None


# инициализация начальных значений переменных db, cursor, чтобы не передавать в каждую функцию
def init_db(file_name):
    global db
    db = sqlite3.connect(file_name)
    global cursor
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS phonebook(
        surname TEXT,
        name TEXT,
        phone TEXT)'''
                   )


# получение информации из БД по запросу sql_qwery. на выходе список кортежей
def get_info(sql_qwery):
    cursor.execute(sql_qwery)
    info = cursor.fetchall()
    return info


# добавление записи в БД. на входе sql-запрос и данные
def add_record(sql_qwery, abonent):
    cursor.execute(sql_qwery, abonent)
    db.commit()


# поиск записи по запросу
def find_record(sql_qwery):
    # pass заглушка
    cursor.execute(sql_qwery)
    info = cursor.fetchall()
    return info


# удаление записи из БД. на входе sql-запрос
def del_record(sql_qwery):
    cursor.execute(sql_qwery)
    db.commit()
