import sqlite3
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("statementbot.json")

client = gspread.authorize(creds)

table = client.open("Statement_bot")
List_1 = table.worksheet("Лист1")


connection = sqlite3.connect('statement.db')
sql = connection.cursor()

sql.execute("CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY AUTOINCREMENT, operator TEXT, inn INTEGER,"
            "client_company_name TEXT, device_number TEXT, comments TEXT, client_number TEXT, client_statement TEXT, "
            "added_date DATETIME, who_updated TEXT, updated_time DATETIME);")


user_connection = sqlite3.connect('all_users.db')
user_sql = user_connection.cursor()

user_sql.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id TEXT, "
                 "operator_name TEXT, number TEXT, added_date DATETIME);")


def check_user(telegram_id):
    user_connection = sqlite3.connect('all_users.db')
    user_sql = user_connection.cursor()

    checker = user_sql.execute("SELECT telegram_id FROM users WHERE telegram_id =?", (telegram_id,)).fetchone()
    if checker:
        return True

    else:
        return False


# Start of Admin page #


def register_user(telegram_id, operator_name, number):
    user_connection = sqlite3.connect('all_users.db')
    user_sql = user_connection.cursor()

    user_sql.execute('INSERT INTO users (telegram_id, operator_name, number, added_date) VALUES (?, ?, ?, ?);',
                (telegram_id, operator_name, number, datetime.now()))

    user_connection.commit()


def get_all_users():
    user_connection = sqlite3.connect('all_users.db')
    user_sql = user_connection.cursor()

    all_users = user_sql.execute('SELECT operator_name FROM users;').fetchall()

    user_names = [i[0] for i in all_users]

    return user_names


def get_user_telegram_id(operator_name):
    user_connection = sqlite3.connect('all_users.db')
    user_sql = user_connection.cursor()

    user_id = user_sql.execute('SELECT telegram_id FROM users WHERE operator_name=?;', (operator_name,)).fetchone()

    return user_id


def get_exact_user(operator_name):
    user_connection = sqlite3.connect('all_users.db')
    user_sql = user_connection.cursor()

    user = user_sql.execute('SELECT * FROM users WHERE operator_name=?;', (operator_name,)).fetchone()

    return user


def delete_exact_user(operator_name):
    user_connection = sqlite3.connect('all_users.db')
    user_sql = user_connection.cursor()

    user_sql.execute('DELETE FROM users WHERE operator_name=?;', (operator_name,))

    user_connection.commit()


def update_exact_user(telegram_id, new_name, new_number, operator_name):
    user_connection = sqlite3.connect('all_users.db')
    user_sql = user_connection.cursor()

    user_sql.execute('UPDATE users SET telegram_id=?, operator_name=?, number=? WHERE operator_name=?;',
                (telegram_id, new_name, new_number, operator_name))

    user_connection.commit()


def update_exact_data(action, new_data, operator_name):
    user_connection = sqlite3.connect('all_users.db')
    user_sql = user_connection.cursor()

    if action == 'Изменить телеграм id':
        user_sql.execute('UPDATE users SET telegram_id=? WHERE operator_name=?;', (new_data, operator_name))

    elif action == 'Изменить имя юзера':
        user_sql.execute('UPDATE users SET operator_name=? WHERE operator_name=?;', (new_data, operator_name))

    elif action == 'Изменить номер телефона':
        user_sql.execute('UPDATE users SET number=? WHERE operator_name=?;', (new_data, operator_name))

    user_connection.commit()

# End of Admin page #


# Start Register client statement #
def client_checker(client_inn):
    connection = sqlite3.connect('statement.db')
    sql = connection.cursor()

    checker = sql.execute('SELECT inn FROM clients WHERE inn=?;', (client_inn,))

    if checker:
        return True

    else:
        return False


def register_client_statement(operator, client_inn, client_company_name, device_number, comments, client_number, client_statement):
    connection = sqlite3.connect('statement.db')
    sql = connection.cursor()

    user_connection = sqlite3.connect('all_users.db')
    user_sql = user_connection.cursor()

    operator_name = user_sql.execute('SELECT operator_name FROM users WHERE telegram_id=?', (operator,)).fetchone()

    if operator_name:

        sql.execute('INSERT INTO clients'
                    '(operator, inn, client_company_name, device_number, comments, client_number, client_statement,'
                    ' added_date)'
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?);',
                    (operator_name[0], client_inn, client_company_name, device_number, comments, client_number,
                     client_statement, datetime.now()))

        connection.commit()

        statement_id = sql.execute('SELECT id FROM clients WHERE inn=?;', (client_inn,)).fetchone()
        print(statement_id)

        List_1.append_row([str(statement_id[0]), operator_name[0], client_inn, client_company_name, device_number,
                           comments, client_number, client_statement, str(datetime.now())])

    else:
        return False


def get_exact_client_statement(client_inn):
    connection = sqlite3.connect('statement.db')
    sql = connection.cursor()

    exact_statement = sql.execute('SELECT * FROM clients WHERE inn=?;', (client_inn,)).fetchall()

    return exact_statement


def get_statement_id(client_inn):
    connection = sqlite3.connect('statement.db')
    sql = connection.cursor()

    statement_id = sql.execute('SELECT id FROM clients WHERE inn=?;', (client_inn,)).fetchall()

    return statement_id


def delete_exact_client_statement(statement_id):
    connection = sqlite3.connect('statement.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM clients WHERE id=?', (statement_id,))

    connection.commit()

    delete_exact_statement = List_1.find(str(statement_id))
    if delete_exact_statement:
        List_1.delete_rows(delete_exact_statement.row)

    else:
        return False


def update_exact_client_statement(statement_id, operator, new_inn, new_client_company_name, new_client_number, new_client_statement):
    connection = sqlite3.connect('statement.db')
    sql = connection.cursor()

    sql.execute('UPDATE clients SET operator=?, inn=?, client_company_name=?, client_number=?, client_statement=?,'
                'WHERE id=?;',
                (operator, new_inn, new_client_company_name, new_client_number, new_client_statement,
                 statement_id))

    connection.commit()

    cell = List_1.find(str(statement_id))

    if cell:
        List_1.update(f'B{cell.row}', operator)
        List_1.update(f'C{cell.row}', new_inn)
        List_1.update(f'D{cell.row}', new_client_company_name)
        List_1.update(f'E{cell.row}', new_client_number)
        List_1.update(f'F{cell.row}', new_client_statement)

    else:
        return False


def update_exact_client_data(statement_id, user_id, action, new_data):
    connection = sqlite3.connect('statement.db')
    sql = connection.cursor()

    user_connection = sqlite3.connect('all_users.db')
    user_sql = user_connection.cursor()

    operator_name = user_sql.execute('SELECT operator_name FROM users WHERE telegram_id=?', (user_id,)).fetchone()

    if operator_name:
        if action == 'Изменить ИНН|ПНФЛ':
            sql.execute('UPDATE clients SET who_updated=?, inn=?, updated_time=? WHERE id=?;',
                        (operator_name[0], new_data, datetime.now(), statement_id))

            cell = List_1.find(str(statement_id))
            if cell:
                time = str(datetime.now())
                List_1.update(f'J{cell.row}', operator_name[0])
                List_1.update(f'C{cell.row}', new_data)
                List_1.update(f'K{cell.row}', time)

        elif action == 'Изменить название фирмы':
            sql.execute('UPDATE clients SET who_updated=?, client_company_name=?, updated_time=? WHERE id=?;',
                        (operator_name[0], new_data, datetime.now(), statement_id))

            cell = List_1.find(str(statement_id))
            if cell:
                time = str(datetime.now())
                List_1.update(f'J{cell.row}', operator_name[0])
                List_1.update(f'D{cell.row}', new_data)
                List_1.update(f'K{cell.row}', time)

        elif action == 'Изменить номер аппарата':
            sql.execute('UPDATE clients SET who_updated=?, device_number=?, updated_time=? WHERE id=?;',
                        (operator_name[0], new_data, datetime.now(), statement_id))

            cell = List_1.find(str(statement_id))
            if cell:
                time = str(datetime.now())
                List_1.update(f'J{cell.row}', operator_name[0])
                List_1.update(f'E{cell.row}', new_data)
                List_1.update(f'K{cell.row}', time)

        elif action == 'Изменить комментарии':
            sql.execute('UPDATE clients SET who_updated=?, comments=?, updated_time=? WHERE id=?;',
                        (operator_name[0], new_data, datetime.now(), statement_id))

            cell = List_1.find(str(statement_id))
            if cell:
                time = str(datetime.now())
                List_1.update(f'J{cell.row}', operator_name[0])
                List_1.update(f'F{cell.row}', new_data)
                List_1.update(f'K{cell.row}', time)

        elif action == 'Изменить номер телефона':
            sql.execute('UPDATE clients SET who_updated=?, client_number=?, updated_time=? WHERE id=?;',
                        (operator_name[0], new_data, datetime.now(), statement_id))

            cell = List_1.find(str(statement_id))
            if cell:
                time = str(datetime.now())
                List_1.update(f'J{cell.row}', operator_name[0])
                List_1.update(f'G{cell.row}', new_data)
                List_1.update(f'K{cell.row}', time)

        elif action == 'Поменять фото заявления':
            sql.execute('UPDATE clients SET who_updated=?, client_statement=?, updated_time=? WHERE id=?;',
                        (operator_name[0], new_data, datetime.now(), statement_id))

            cell = List_1.find(str(statement_id))
            if cell:
                time = str(datetime.now())
                List_1.update(f'J{cell.row}', operator_name[0])
                List_1.update(f'H{cell.row}', new_data)
                List_1.update(f'K{cell.row}', time)

        else:
            return "Что то пошло не так!"

    connection.commit()
