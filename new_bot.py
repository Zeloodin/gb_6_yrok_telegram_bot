import telebot
# from random import *
# import json
# import requests

from g4f.client import Client

API_TOKEN = YOUR_API_TOKEN # Токен от BotFather
bot = telebot.TeleBot(API_TOKEN)
mode_on_off = False

@bot.message_handler(commands=['start','startrun','help']) # стартовая команда.
def start_message(message):
    bot.send_message(message.chat.id, """
Команды:
/startbot включает бот. Вы можете просто отправлять текст, а чатГПТ отвечать на ваши запросы.
/stopbot выключает бот. Выключает чатГПТ. Он не реагирует на ваши сообшения.
/help показывает какие есть команды и описания к ней.
""")


@bot.message_handler(commands=['startbot'])
def enable_bot(message):
    global mode_on_off # Глобально открывает переменную.
    mode_on_off = True # Присваивание True, в переменную mode_on_off
    bot.send_message(message.chat.id, "чатГПТ, включен") # Отправка текста в чат телеграм, от имени чат бота

@bot.message_handler(commands=['stopbot'])
def disable_bot(message):
    global mode_on_off # Глобально открывает переменную.
    mode_on_off = False # Присваивание False, в переменную mode_on_off
    bot.send_message(message.chat.id, "чатГПТ, выключен") # Отправка текста в чат телеграм, от имени чат бота

@bot.message_handler(content_types=['text'])
def open_bot(message): # Бот включен
    if mode_on_off: # Если значение True, то чат отвечает на текст пользователя. Иначе, ничего не делает.
        input_message = " ".join(str(message.text).split(" ")[:]) # берёт сообщение
        bot.send_message(message.chat.id, "Отправлен запрос в chatGPT, пожалуйста подождите") # Отправка текста в чат телеграм, от имени чат бота

        client = Client() # создаётся ГПТчат Клиет
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # выбор модели, для выполнение запроса для пользователя
            messages=[{"role": "user", "content": f"{input_message}"}] # сообщение пользователя для отправки чатГПТ
        )
        # print(response.choices[0].message.content) # Получение результа от чатГПТ в консоль
        bot.send_message(message.chat.id, response.choices[0].message.content) # Получение результа от чатГПТ в чат Телеграм
    else:
        pass # Не реагирует. Пропускает.




bot.polling()