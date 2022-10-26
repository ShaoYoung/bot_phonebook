# Обработка событий от пользователя, изменение модели

import model as mod

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import datetime

filename = 'db.log'
def log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open(filename, 'a', encoding="utf-8") as file:
        file.write(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}, {update.effective_user.first_name}, {update.effective_user.id}, {update.message.text}\n')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log(update, context)
    out_text = f'/help - помощь\n/view - просмотреть базу\n/add - добавить абонента (ex. /add Ivanov Ivan 222333)\n/find - найти абонента (ex. /find Ivanov)\n' \
               f'/del - удалить абонента (ex. /del Ivanov)'
    await update.message.reply_text(out_text)


async def view_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log(update, context)
    info = mod.get_info('SELECT * FROM phonebook')
    # print(info)
    out_text = ''
    for abonent in info:
        out_text += f'{(" ").join(abonent)}\n'
        # print(out_text)
    if not len(out_text):
        out_text = 'Ничего не найдено'
    await update.message.reply_text(out_text)


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log(update, context)
    msg = update.message.text
    abonent = get_data(msg)
    out_text = 'В БД ничего не добавлено'
    for i in abonent:
        if len(i):
            mod.add_record('INSERT INTO phonebook VALUES(?, ?, ?);', abonent)
            out_text = f'В БД добавлен {(" ").join(abonent)}\n'
            break
    await update.message.reply_text(out_text)


async def find_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log(update, context)
    msg = update.message.text
    # для поиска берём первый элемент из запроса пользователя
    record = get_data(msg)[0]
    # print(record)
    column = ['surname', 'name', 'phone']
    out_text = ''
    # поочерёдно ищем совпадение по всем столбцам БД
    for i in column:
        info = mod.find_record(
            f'SELECT * FROM phonebook WHERE "{i}" LIKE "{record}"')  # LIKE - поиск по шаблону
        # print(info)
        if len(info) > 0:
            for abonent in info:
                out_text += f'{(" ").join(abonent)}\n'
            # после нахождения первой записи в БД прерываемся. МОЖНО ПОПРОБОВАТЬ ИСКАТЬ ДАЛЬШЕ В ОСТАЛЬНЫХ СТОЛБЦАХ
            # break     # если убрать break, будет искать по всем столбцам
    if not len(out_text):
        out_text = 'Ничего не найдено'
    await update.message.reply_text(out_text)


async def del_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log(update, context)
    msg = update.message.text
    # для поиска берём первый элемент из запроса пользователя
    record = get_data(msg)[0]
    # print(record)
    column = ['surname', 'name', 'phone']
    out_text = ''
    # поочерёдно ищем совпадение по всем столбцам БД
    for i in column:
        info = mod.find_record(f'SELECT * FROM phonebook WHERE "{i}" LIKE "{record}"')
        # LIKE - поиск по шаблону
        # print(i, '-', record, '-', info)
        # если запись есть в БД, то удаляем запись в найденном столбце БД
        if len(info) > 0:
            mod.del_record(f'DELETE FROM phonebook WHERE "{i}" = "{record}"')
            # print(i, '-', record, '-', info)
            # и записываем строку для вывода пользователю
            for abonent in info:
                out_text += f'{(" ").join(abonent)}\n'
                # print(out_text)
            # после нахождения первой записи в БД прерываемся. МОЖНО ПОПРОБОВАТЬ ИСКАТЬ ДАЛЬШЕ В ОСТАЛЬНЫХ СТОЛБЦАХ
            # break     # если убрать break, будет искать по всем столбцам
    if not len(out_text):
        out_text = 'Из БД ничего не удалено'
    else:
        out_text = f'Из БД удалено:\n{out_text}'

    await update.message.reply_text(out_text)


# начало работы controller, инициализация БД
def start_work():
    file_name = 'Data_base.db'
    mod.init_db(file_name)


# получение информации от бота. на выходе список
def get_data(msg):
    if msg.find(' ') != -1:
        msg = msg.split()
        # убираем команду из сообщения
        msg.pop(0)
        while len(msg) < 3:
            msg.append('')
        return msg
    else:
        return ['', '', '']





# просмотр БД
# def preview_base():
#     info = mod.get_info('SELECT * FROM phonebook')
#     vt.print_db(info)


# добавление информации в БД
# def add_db():
#     # получаем новую запись БД
#     abonent = list(vt.get_data('нового').values())
#     # print(worker)
#     mod.add_record('INSERT INTO phonebook VALUES(?, ?, ?);', abonent)


# поиск информации в БД
# def find_info():
#     print('Буду искать информацию. Заполните одно поле БД. Ищу по первому совпадению!')
#     worker = vt.get_data('искомого')
#     # print(worker)
#     # ищем первый столбец, в какое поле БД пользователь ввёл данные
#     for key in worker:
#         if worker[key] != '' and worker[key] != None:
#             column = key
#             value = worker[key]
#             info = mod.find_record(
#                 f'SELECT * FROM phonebook WHERE "{column}" LIKE "{value}"')  # LIKE - поиск по шаблону
#             break
#             # print(column, value)
#             # print(type(column), type(value))
#     print('Нашёл:')
#     # показываем найденную запись
#     if not len(info):
#         print('Запрашиваемой информации нет в БД!')
#         return []
#     else:
#         vt.print_db(info)
#         return [column, value]


# удаление информации из БД
# def del_info():
#     # ищем запись БД
#     info = find_info()
#     # если есть записи БД
#     if len(info):
#         # контрольный вопрос для подтверждения удаления записи
#         accept_delete = input('Удаляем? 1 - Да, 0 - Нет: --> ')
#         # print(type(info[0]), '-', type(info[1]))
#         # print(info[0], '-', info[1])
#         if int(accept_delete):
#             mod.del_record(f'DELETE FROM personal WHERE "{info[0]}" = "{info[1]}"')
#
#
# выгрузка БД в json-файл
# def save_json():
#     pass
# """
# :param: В будущем можно выгружать любую выборку из БД
# :return: write file
# """
# # получаем всю БД
# info = mod.get_info('SELECT * FROM phonebook')
# # делаем из списка словарь (key - номер записи работника, value - данные из БД)
# worker_json = {}
# for count in range(1, len(info) + 1):
#     worker_json[count] = info[count - 1]
# print(f'В файл будет записан следующий словарь: {worker_json}')
# file_name = 'db.json'
# with open(file_name, mode='w') as jsonfile:
#     # преобразовываем объект Python в данные формата JSON и записываем в файл phone_book.json обновлённый справочник
#     json.dump(worker_json, jsonfile)
