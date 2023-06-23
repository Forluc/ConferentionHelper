import telebot
from environs import Env
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

Env().read_env()
token = Env().str('TG_SPEAKERS_BOT_TOKEN')
bot = telebot.TeleBot(token)

# Получение данных из БД
questions = ['questions', 'questions1', 'questions2', 'questions3']  # TODO Нужен список вопросов из БД
speakers = ['da_maslyaev', 'TemWithFrog', 'SammelsFavillion', 'vladpap']  # TODO Нужен список докладчиков из БД
count = len(questions)
page = 1


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global page
    global count
    global questions
    global speakers
    # Обработка кнопки - скрыть
    if call.data == 'unseen':
        bot.delete_message(call.message.chat.id, call.message.message_id)
    # Обработка кнопки - готовность ответа на вопросы
    elif call.data == 'verify':
        if call.from_user.username in speakers:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text='Готов', callback_data='main'))
            bot.send_message(call.message.chat.id, 'Готов отвечать на вопросы?', reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id,
                             'Уточни у организатора, внес ли он тебя в список докладчиков, и перезапусти бот')

    # Обработка кнопки - меню вопросов
    elif call.data == 'main':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Закончить доклад',
                                        callback_data='finish'))
        markup.add(InlineKeyboardButton(text=f'<--- Назад', callback_data=f'back-page'),
                   InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                   InlineKeyboardButton(text=f'Вперёд --->', callback_data=f'next-page'))
        bot.edit_message_text(questions[page - 1], reply_markup=markup,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)

    # Обработка кнопки - вперед
    elif call.data == 'next-page':
        if page < count:
            page = page + 1
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text='Закончить доклад',
                                            callback_data='finish'))
            markup.add(InlineKeyboardButton(text=f'<--- Назад', callback_data=f'back-page'),
                       InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                       InlineKeyboardButton(text=f'Вперёд --->', callback_data=f'next-page'))
            bot.edit_message_text(questions[page - 1], reply_markup=markup,
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
    # Обработка кнопки - назад
    elif call.data == 'back-page':
        if page > 1:
            page = page - 1
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text='Закончить доклад',
                                            callback_data='finish'))
            markup.add(InlineKeyboardButton(text=f'<--- Назад', callback_data=f'back-page'),
                       InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                       InlineKeyboardButton(text=f'Вперёд --->', callback_data=f'next-page'))
            bot.edit_message_text(questions[page - 1], reply_markup=markup,
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
    # Обработка кнопки - Закончить доклад
    if call.data == 'finish':  # TODO Добавить отметку в БД Закончить доклад
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(text='Хочу', url='https://t.me/MeetUsers_bot'))
        bot.send_message(call.message.chat.id, 'Хочешь послушать других докладчиков?', reply_markup=markup)


# Обработчик начала использования бота
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Подтвердить', callback_data='verify'))
    bot.send_message(message.from_user.id, "Привет, если ты докладчик, подтверди", reply_markup=markup)


bot.polling(none_stop=True)
