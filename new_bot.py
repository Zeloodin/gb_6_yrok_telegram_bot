import telebot
# from random import *
# import json
# import requests
import g4f
from g4f.client import Client

API_TOKEN = "YOUR_API_TOKEN" # Токен от BotFather
bot = telebot.TeleBot(API_TOKEN)
mode_on_off = False
first_start = True
new_dialog = True

@bot.message_handler(commands=['start','startrun','help']) # стартовая команда.
def start_message(message):
    bot.send_message(message.chat.id, """
Команды:
/startbot включает бот. Вы можете просто отправлять текст, а чатГПТ отвечать на ваши запросы.
/stopbot выключает бот. Выключает чатГПТ. Он не реагирует на ваши сообшения.
/newdialog. Всегда будет с чистой памятью принимать запросы, без памяти о предыдущих сообщений.
/olddialog. Всегда будет запоминать все запросы.
/help показывает какие есть команды и описания к ней.
""")


@bot.message_handler(commands=['startbot'])
def enable_bot(message):
    global mode_on_off, first_start # Глобально открывает переменную.
    mode_on_off = True # Присваивание True, в переменную mode_on_off
    first_start = True # Запускается при первом запуске, чат бота.
    bot.send_message(message.chat.id, "чатГПТ, включен") # Отправка текста в чат телеграм, от имени чат бота

@bot.message_handler(commands=['stopbot'])
def disable_bot(message):
    global mode_on_off # Глобально открывает переменную.
    mode_on_off = False # Присваивание False, в переменную mode_on_off
    bot.send_message(message.chat.id, "чатГПТ, выключен") # Отправка текста в чат телеграм, от имени чат бота


@bot.message_handler(commands=['newdialog'])
def enable_new_dialog(message):
    global new_dialog # Глобально открывает переменную.
    new_dialog = True # Включает режим новый диалог, не помнит старые сообщения.
    bot.send_message(message.chat.id, "Новый запрос, не помнит предыдущие сообщения") # Отправка текста в чат телеграм, от имени чат бота

@bot.message_handler(commands=['olddialog'])
def disable_new_dialog(message):
    global new_dialog # Глобально открывает переменную.
    new_dialog = False # Выключает режим новый диалог, помнит старые сообщения.
    bot.send_message(message.chat.id, "Помнит старые запросы, при новом запросе") # Отправка текста в чат телеграм, от имени чат бота



@bot.message_handler(content_types=['text'])
def open_bot(message): # Бот включен
    global new_dialog, first_start, client
    if mode_on_off: # Если значение True, то чат отвечает на текст пользователя. Иначе, ничего не делает.
        input_message = " ".join(str(message.text).split(" ")[:]) # берёт сообщение
        bot.send_message(message.chat.id, "Отправлен запрос в chatGPT, пожалуйста подождите") # Отправка текста в чат телеграм, от имени чат бота
        if new_dialog or first_start: # срабатывает, при первом запуске, и или с режимом новый диалог.
            client = Client() # создаётся ГПТчат Клиет
            first_start = False
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", # выбор модели, для выполнение запроса для пользователя
                messages=[{"role": "user", "content": f"{input_message}"}], # сообщение пользователя для отправки чатГПТ
                max_tokens=512 # Максимальное колличество токенов
            )
            # print(response.choices[0].message.content) # Получение результа от чатГПТ в консоль
            bot.send_message(message.chat.id, response.choices[0].message.content) # Получение результата от чатГПТ в чат Телеграм

        except g4f.errors.RetryProviderError:
            bot.send_message(message.chat.id,
"""Простите. Ваш запрос не был обработан.
В связи с большим запросом.
Пожалуйста, коротко запросы отправляйте.
ЧатГПТ не справляется с большим запросом.
Спасибо за понимание.""")  # Вывод сообщение вместо ошибки.

    else:
        pass # Не реагирует. Пропускает.




bot.polling()