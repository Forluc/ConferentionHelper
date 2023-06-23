import telebot
from environs import Env
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

Env().read_env()
token = Env().str('TG_USERS_BOT_TOKEN')
bot = telebot.TeleBot(token)

# -------------------Получение данных от пользователя из бота-----------------------------
users_data = {
    'name': None,
    'phone_number': None,
    'username': None,
    'tg_id': None,
}

# -------------------Получение данных из БД-----------------------------

# Получение списка телеграм id пользователей
users_id = [1827882264, 721137092]  # TODO наполнить данными из БД
# Получение словаря спикера который выступает сейчас
speaker_details = {  # TODO наполнить данными из БД
    'speaker': 'Иван Петров',
    'date': '2023-06-22',
    'start_time': '09:00',
    'end_time': '09:45',
    'lecture': 'Как стать востребованным Python-разработчиком?',
    'description': 'Что на самом деле нужно, чтобы стать ценным специалистом и найти работу?',
}
# Получение списка словарей(ключ-дата события, значение список из времени)
programs = [{'2023-06-22': ['09:00 - 09:45', '10:05 - 10:45']},
            {'2023-06-22': ['15:05 - 15:45']}]  # TODO наполнить данными из БД
speaker_names = ['Иван Петров', 'Федя Спикеров']  # TODO наполнить данными из БД
# Получение списка всех выступлений спикеров
speakers = {  # TODO наполнить данными из БД
    'Иван Петров': [
        {'date': '2023-06-22', 'start_time': '09:00', 'end_time': '09:45',
         'lecture': 'Как стать востребованным Python-разработчиком?',
         'description': 'Что на самом деле нужно, чтобы стать ценным специалистом и найти работу?',
         },
        {'date': '2023-06-23', 'start_time': '10:00', 'end_time': '11:45',
         'lecture': 'Java',
         'description': 'Идем вверх',
         }
    ],
    'Федя Спикеров': [
        {'date': '2023-06-22', 'start_time': '12:00', 'end_time': '12:45',
         'lecture': 'Python-разработчик',
         'description': 'Найти работу?',
         },
        {'date': '2023-06-23', 'start_time': '15:00', 'end_time': '15:45',
         'lecture': 'Kotlin',
         'description': 'Идем дальше',
         }
    ]
}


# Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    def ggg():
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Спикеры и программа', callback_data='speakers-and-programs'))
        markup.add(InlineKeyboardButton(text='Сейчас выступает', callback_data='now-speaker'))
        markup.add(InlineKeyboardButton(text='На главную', callback_data='main'))
        bot.send_photo(call.message.chat.id,
                       r'https://blog.europython.eu/content/images/size/w1000/2023/04/default.png',
                       reply_markup=markup,
                       caption='Спикеры заранее записываются, чтобы выступить, готовят презентации на тему Python и разработки в целом, приглашается много гостей, спикеры рассказывают презентации, гости задают вопросы, в конце – все кушают бесплатную пиццу и обмениваются визитками.')

    # Обработка кнопки - меню
    if call.data == 'main':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='О конференции', callback_data='about-us'))
        markup.add(InlineKeyboardButton(text='Спикеры и программа', callback_data='speakers-and-programs'))
        markup.add(InlineKeyboardButton(text='Сейчас выступает', callback_data='now-speaker'))
        bot.send_photo(call.message.chat.id,
                       r'https://blog.europython.eu/content/images/size/w1000/2023/04/default.png', reply_markup=markup,
                       caption='Мы рады видеть Вас среди участников конференции')
    # Обработка кнопки - спикеры и программа
    elif call.data == 'speakers-and-programs':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Спикеры', callback_data='speakers'))
        markup.add(InlineKeyboardButton(text='Программа', callback_data='programs'))
        markup.add(InlineKeyboardButton(text='На главную', callback_data='main'))
        bot.send_message(call.message.chat.id, 'Выберете интересующий Вас раздел', reply_markup=markup)
    # Обработка кнопки - программа
    elif call.data == 'programs':
        for full_program in programs:
            for date, program in full_program.items():
                form_program = '\n'.join(map(str, program))
                bot.send_message(call.message.chat.id, f"{date}\n{form_program}")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='На главную', callback_data='main'))
        bot.send_message(call.message.chat.id, text='Перейти на главную?', reply_markup=markup)
    # Обработка кнопки - спикеры
    elif call.data == 'speakers':
        markup = InlineKeyboardMarkup()
        for speaker, lectures in speakers.items():
            markup.add(InlineKeyboardButton(text=speaker, callback_data='about-speaker'))
        main = markup.add(InlineKeyboardButton(text='На главную', callback_data='main'))
        send = bot.send_message(call.message.chat.id, 'Какой спикер вас интересует?', reply_markup=markup)
    # Обработка кнопки - о конференции
    elif call.data == 'about-us':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Спикеры и программа', callback_data='speakers-and-programs'))
        markup.add(InlineKeyboardButton(text='Сейчас выступает', callback_data='now-speaker'))
        markup.add(InlineKeyboardButton(text='На главную', callback_data='main'))
        bot.send_photo(call.message.chat.id,
                       r'https://blog.europython.eu/content/images/size/w1000/2023/04/default.png',
                       reply_markup=markup,
                       caption='Спикеры заранее записываются, чтобы выступить, готовят презентации на тему Python и разработки в целом, приглашается много гостей, спикеры рассказывают презентации, гости задают вопросы, в конце – все кушают бесплатную пиццу и обмениваются визитками.')
    # Обработка кнопки - сейчас выступает
    elif call.data == 'now-speaker':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Задать вопрос', callback_data='question'))
        markup.add(InlineKeyboardButton(text='На главную', callback_data='main'))
        bot.send_message(call.message.chat.id,
                         f"Спикер:\n{speaker_details['speaker']}\n\n{speaker_details['date']}\n{speaker_details['start_time']}-{speaker_details['end_time']}\n\nДоклад на тему:\n{speaker_details['lecture']}\n\n{speaker_details['description']}",
                         reply_markup=markup)
    # Обработка кнопки - задать вопрос
    elif call.data == 'question':
        sent = bot.send_message(call.message.chat.id,
                                f"Спикер: {speaker_details['speaker']}\nДоклад: {speaker_details['lecture']}\nВведите ниже ваш вопрос:")
        bot.register_next_step_handler(sent, get_question)
    # Обработка кнопки - получение программы определенного спикера
    elif call.data == 'about-speaker':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='На главную', callback_data='main'))
        bot.send_message(call.message.chat.id, f'Пойти на клавную?', reply_markup=markup)


# Обработчик входящих сообщений
@bot.message_handler(commands=['start'])
def start(message):
    users_data['username'] = message.from_user.username
    users_data['tg_id'] = message.from_user.id
    sent = bot.send_message(message.from_user.id, 'Привет, как тебя зовут?')
    bot.register_next_step_handler(sent, get_name_user)


def get_name_user(message):
    users_data['name'] = message.text
    sent = bot.send_message(message.from_user.id, f"Отлично, {users_data['name']}, а теперь введи номер телефона")
    bot.register_next_step_handler(sent, get_phone_number)


def get_phone_number(message):
    users_data['phone_number'] = message.text
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Продолжить', callback_data='main'))
    bot.send_message(message.from_user.id, "Отлично, все данные введены, нажми продолжить", reply_markup=markup)


# Функция для отправки вопроса в БД
def get_question(message):
    question = message.text
    user = message.from_user.username
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Сейчас выступает', callback_data='now-speaker'))
    markup.add(InlineKeyboardButton(text='На главную', callback_data='main'))
    bot.send_message(message.from_user.id, "Ваш вопрос отправлен", reply_markup=markup)
    print(question, user, speaker_details['speaker'])  # TODO сделать отправку вопросов в БД


# Отправка массовых уведомлений об изменении программы докладов
@bot.message_handler(commands=['update'])
def update(message):
    if message.from_user.id in [721137092, ]:  # TODO Добавить в список, тех, кто будет отправлять рассылку
        for user_id in users_id:
            bot.send_message(user_id, 'Поменялась программа выступления, посмотрите изменения')


bot.polling(none_stop=True)
