from telebot import types
import database


def main_menu_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    button_1 = types.KeyboardButton('Найти заявления клиента')
    button_2 = types.KeyboardButton('Добавить заявления')

    kb.add(button_1, button_2)

    return kb


def action_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button_1 = types.KeyboardButton('Редактировать')
    button_2 = types.KeyboardButton('Удалить')
    button_3 = types.KeyboardButton('Назад')

    kb.add(button_1, button_2, button_3)

    return kb


def confirm_action():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button_1 = types.KeyboardButton('Потвердить')
    button_2 = types.KeyboardButton('Назад')

    kb.add(button_1, button_2)

    return kb


def user_select_action_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    button_1 = types.KeyboardButton('Изменить ИНН|ПНФЛ')
    button_2 = types.KeyboardButton('Изменить название фирмы')
    button_3 = types.KeyboardButton('Изменить номер аппарата')
    button_4 = types.KeyboardButton('Изменить комментарии')
    button_5 = types.KeyboardButton('Изменить номер телефона')
    button_6 = types.KeyboardButton('Поменять фото заявления')

    kb.add(button_1, button_2, button_3, button_4, button_5, button_6)

    return kb


# Admin side buttons #


def register_user_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button_1 = types.KeyboardButton('Добавить юзера')
    button_2 = types.KeyboardButton('Изменить данные юзера')
    button_3 = types.KeyboardButton('Удалить юзера')

    kb.add(button_1, button_2, button_3)

    return kb


def back_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button_1 = types.KeyboardButton('Назад')
    kb.add(button_1)

    return kb


def update_data_exact_user():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button_1 = types.KeyboardButton('Изменить телеграм id')
    button_2 = types.KeyboardButton('Изменить имя юзера')
    button_4 = types.KeyboardButton('Изменить номер телефона')
    button_5 = types.KeyboardButton('Назад')

    kb.add(button_1, button_2, button_4, button_5)

    return kb


def get_all_users_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    all_users = database.get_all_users()
    for user in all_users:
        kb.add(user)

    button_1 = types.KeyboardButton('Назад')
    kb.add(button_1)
    return kb
