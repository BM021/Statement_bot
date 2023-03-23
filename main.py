import telebot
from telebot import types

import buttons
import database

bot = telebot.TeleBot('')


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    text = f'Привет!\n\nВыберите нужный пункт'

    checker = database.check_user(user_id)
    if checker:
        bot.send_message(user_id, text, reply_markup=buttons.main_menu_buttons())

    else:
        bot.send_message(user_id, 'Походу вы ошиблись с дверью!')


@bot.message_handler(commands=['admin'])
def admin_menu(message):
    user_id = 777322005
    text = 'Добро пожаловать Супер Админ!'

    if message.from_user.id == user_id:
        bot.send_message(user_id, text, reply_markup=buttons.register_user_buttons())


@bot.message_handler(content_types=['text'])
def text_messages(message):
    admin_id = 777322005

# Admin
    if message.from_user.id == admin_id:
        if message.text == 'Добавить юзера':
            bot.send_message(admin_id, 'Введите id оператора', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, get_user_telegram_id)

        elif message.text == 'Изменить данные юзера':
            bot.send_message(admin_id, 'Выберите юзера', reply_markup=buttons.get_all_users_button())
            bot.register_next_step_handler(message, update_exact_user)

        elif message.text == 'Удалить юзера':
            bot.send_message(admin_id, 'Выберите юзера', reply_markup=buttons.get_all_users_button())
            bot.register_next_step_handler(message, delete_exact_user)

        elif message.text == 'Назад':
            text_messages(message)


# Users
    if message.text == 'Добавить заявления':
        register_statement(message)

    elif message.text == 'Найти заявления клиента':
        bot.send_message(message.from_user.id, 'Введите ИНН|ПНФЛ', reply_markup=buttons.back_button())
        bot.register_next_step_handler(message, find_exact_statement)


# Admin side #
def get_user_telegram_id(message):
    admin_id = 777322005
    telegram_id = int(message.text)

    bot.send_message(admin_id, 'Введите имя оператора')
    bot.register_next_step_handler(message, get_user_name, telegram_id)


def get_user_name(message, telegram_id):
    admin_id = 777322005
    operator_name = message.text

    bot.send_message(admin_id, 'Введите телефон номер операвтора')
    bot.register_next_step_handler(message, get_user_number, telegram_id, operator_name)


def get_user_number(message, telegram_id, operator_name):
    admin_id = 777322005
    number = message.text

    checker = database.check_user(telegram_id)

    if checker:
        bot.send_message(admin_id, 'Такой юзер есть!', reply_markup=buttons.register_user_buttons())

    else:
        database.register_user(telegram_id, operator_name, number)
        bot.send_message(admin_id, 'Успешно зареган!', reply_markup=buttons.register_user_buttons())


def update_exact_user(message):
    admin_id = 777322005
    update_user = message.text

    bot.send_message(admin_id, 'Выберите действие', reply_markup=buttons.update_data_exact_user())
    bot.register_next_step_handler(message, update_action, update_user)


def update_action(message, update_user):
    admin_id = 777322005
    action = message.text

    bot.send_message(admin_id, 'Введинте новые данные', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, update_exact_user_data, update_user, action)


def update_exact_user_data(message, update_user, action):
    admin_id = 777322005
    new_data = message.text

    database.update_exact_data(action, new_data, update_user)
    bot.send_message(admin_id, 'Успешно обновлено!', reply_markup=buttons.register_user_buttons())


def delete_exact_user(message):
    admin_id = 777322005

    delete_user = message.text
    database.delete_exact_user(delete_user)
    bot.send_message(admin_id, 'Успешно удалено!', reply_markup=buttons.register_user_buttons())

# End Admin side #


# Start users side #
def register_statement(message):
    user_id = message.from_user.id

    bot.send_message(user_id, 'Введите ИНН/ПНФЛ клиента', reply_markup=buttons.back_button())
    bot.register_next_step_handler(message, get_client_company_name, user_id)


def get_client_company_name(message, user_id):
    client_inn = message.text

    if message.text == 'Назад':
        bot.send_message(user_id, 'Вы вернулись назад', reply_markup=buttons.main_menu_buttons())

    elif message.photo:
        bot.send_message(user_id, 'Отправьте ИНН или ПНФЛ')
        bot.register_next_step_handler(message, get_client_company_name, user_id)

    else:
        bot.send_message(user_id, 'Введите название фирмы', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_client_device_number, user_id, client_inn)


def get_client_device_number(message, user_id, client_inn):
    company_name = message.text

    if message.photo:
        bot.send_message(user_id, 'Фото не принемается, отправьте в текстовом виде')
        bot.register_next_step_handler(message, get_client_device_number, user_id, client_inn)

    else:
        bot.send_message(user_id, 'Введите номер аппарата')
        bot.register_next_step_handler(message, get_client_comment, user_id, client_inn, company_name)


def get_client_comment(message, user_id, client_inn, company_name):
    client_device_number = message.text

    if message.photo:
        bot.send_message(user_id, 'Фото не принемается, отправьте в текстовом виде')
        bot.register_next_step_handler(message, get_client_comment, user_id, client_inn, company_name)

    else:
        bot.send_message(user_id, 'Введите комментарий, если нет то 0')
        bot.register_next_step_handler(message, get_client_number, user_id, client_inn, company_name,
                                       client_device_number)


def get_client_number(message, user_id, client_inn, company_name, client_device_number):
    client_comment = message.text

    bot.send_message(user_id, 'Введите номер телефона клиента, если нет то 0')
    bot.register_next_step_handler(message, get_client_statement, user_id, client_inn, company_name,
                                   client_device_number, client_comment)


def get_client_statement(message, user_id, client_inn, company_name,  client_device_number, client_comment):
    client_number = message.text

    bot.send_message(user_id, 'Отправьте фото заявления')
    bot.register_next_step_handler(message, get_statement_photo, user_id, client_inn, company_name,
                                   client_device_number, client_comment, client_number)


def get_statement_photo(message, user_id, client_inn, company_name, client_device_number, client_comment,
                        client_number):

    if message.photo:
        database.register_client_statement(user_id, client_inn, company_name, client_device_number, client_comment,
                                           client_number, message.photo[-1].file_id)

        bot.send_message(user_id, 'Успешно зареган!', reply_markup=buttons.main_menu_buttons())

    else:
        bot.send_message(user_id, 'Отправьте другой')
        bot.register_next_step_handler(message, get_statement_photo, user_id, client_inn, company_name,
                                       client_device_number, client_comment, client_number)


def find_exact_statement(message):
    user_id = message.from_user.id
    client_inn = message.text

    if message.text == 'Назад':
        bot.send_message(user_id, 'Вы вернулись назад', reply_markup=buttons.main_menu_buttons())

    else:

        exact_statement = database.get_exact_client_statement(client_inn)

        if exact_statement:
            for mess in exact_statement:
                full_message = f'ID: {mess[0]}\n\n' \
                                f'Клиента добавил: {mess[1]}\n\n' \
                                f'ИНН|ПНФЛ: {mess[2]}\n\n' \
                                f'Название фирмы: {mess[3]}\n\n' \
                                f'Номер аппарата: {mess[4]}\n\n' \
                                f'Комментарий: {mess[5]}\n\n' \
                                f'Номер телефона: {mess[6]}\n\n' \
                                f'Дата добавления: {mess[8]}\n\n' \
                                f'Кто изменил: {mess[9]}\n\n' \
                                f'Дата изменения: {mess[10]}'

                bot.send_photo(user_id, photo=mess[7], caption=full_message,
                               reply_markup=buttons.action_buttons())

            bot.register_next_step_handler(message, get_id_statement, client_inn)

        else:
            bot.send_message(user_id, 'Не могу найти', reply_markup=buttons.main_menu_buttons())


def get_id_statement(message, client_inn):
    user_id = message.from_user.id
    action = message.text

    if action == 'Назад':
        bot.send_message(user_id, 'Вы вернулись назад', reply_markup=buttons.main_menu_buttons())

    else:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

        id_buttons = database.get_statement_id(client_inn)

        for btn in id_buttons:
            kb.add(str(btn[0]))

        bot.send_message(user_id, 'Выберите id заявления', reply_markup=kb)
        bot.register_next_step_handler(message, get_action, action)


def get_action(message, action):
    user_id = message.from_user.id
    statement_id = int(message.text)

    if action == 'Назад':
        bot.send_message(user_id, 'Вы вернулись назад', reply_markup=buttons.main_menu_buttons())

    elif action == 'Редактировать':
        bot.send_message(user_id, 'Выберите нужный пункт', reply_markup=buttons.user_select_action_buttons())
        bot.register_next_step_handler(message, get_update_exact_data, statement_id)

    elif action == 'Удалить':
        bot.send_message(user_id, 'Вы точно хотите удалить?', reply_markup=buttons.confirm_action())
        bot.register_next_step_handler(message, get_accept, statement_id)


def get_accept(message, statement_id):

    if message.text == 'Потвердить':
        database.delete_exact_client_statement(statement_id)
        bot.send_message(message.from_user.id, 'Успешно удалено!', reply_markup=buttons.main_menu_buttons())

    else:
        bot.send_message(message.from_user.id, 'Удаление отменина', reply_markup=buttons.main_menu_buttons())


def get_update_exact_data(message, statement_id):
    action = message.text
    user_id = message.from_user.id

    if action == 'Поменять фото заявления':
        bot.send_message(user_id, 'Отправьте новые фото заявления')
        bot.register_next_step_handler(message, get_update_exact_client_data, statement_id, user_id, action)

    else:
        bot.send_message(user_id, 'Введите новые данные')
        bot.register_next_step_handler(message, get_update_exact_client_data, statement_id, user_id, action)


def get_update_exact_client_data(message, statement_id, user_id, action):

    if message.photo:
        new_photo = message.photo[-1].file_id
        database.update_exact_client_data(statement_id, user_id, action, new_photo)
        bot.send_message(user_id, 'Успешно обновлено!', reply_markup=buttons.main_menu_buttons())

    else:
        new_data = message.text

        database.update_exact_client_data(statement_id, user_id, action, new_data)
        bot.send_message(user_id, 'Успешно обновлено!', reply_markup=buttons.main_menu_buttons())


# bot.polling()
while True:
    if __name__ == "__main__":
        try:
             bot.polling(none_stop=True)

        except Exception as ex:
             print(ex)
