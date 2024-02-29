import requests
from telebot import types
from info import botus
def post(text, bot):
    resp = requests.post(
        'http://localhost:1234/v1/chat/completions',
        headers={"Content-Type": "application/json"},
        json={
            "messages": [
                {"role": "system",
                 "content": botus[bot]},
                {"role": "user", "content": text},
            ],
            "temperature": 0.1,
        }
    )
    return resp
def nez():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("завершить")
    btn2 = types.KeyboardButton("продолжить")
    markup.add(btn1, btn2)
    return markup
def set():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("помощник по математике")
    btn2 = types.KeyboardButton("помощник по программированию")
    btn3 = types.KeyboardButton("обычный")
    markup.add(btn1, btn2, btn3)
    return markup
