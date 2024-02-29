import telebot
import logging
from info import information, boty
from bot_func import post, nez, set
from config import token

bot = telebot.TeleBot(token=token)
users = {}
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w",
)
def add_user(id):
    if not id in users:
        users[id] = {"debug": False, "bot" : "prog", "vvod" : False}
@bot.message_handler(content_types = ['text'])
def vvod(message):
    add_user(message.chat.id)
    if users[message.chat.id]["vvod"] == False:
        if message.text == "/start":
            logging.info("start")
            bot.send_message(message.chat.id, information["/start"])
        elif message.text == "/send":
            bot.register_next_step_handler(message, gpt)
            logging.info("/send")
        elif message.text == "/settings":
            markup = set()
            bot.send_message(message.chat.id, "Выбери помощника", reply_markup=markup)
            logging.info("/settings")
            bot.register_next_step_handler(message, vybor)
        elif message.text == "/debug":
            if users[message.chat.id]["debug"] == False:
                users[message.chat.id]["debug"] = True
                logging.info("debug режим включен")
                bot.send_message(message.chat.id, "вы включили Debug")
                with open("log_file.txt", "rb") as f:
                    bot.send_document(message.chat.id, f)
            elif users[message.chat.id]["debug"] == True:
                users[message.chat.id]["debug"] = False
                logging.info("debug режим выключен")
                bot.send_message(message.chat.id, "вы выключили Debug")

        else:
            bot.send_message(message.chat.id, "не знаю такой команды")
            logging.info("неизвестная команда")
    else:
        bot.send_message(message.chat.id, "подождите пока бот отправит ответ")
        logging.info("Ожидание ответа")
def gpt(message):
    users[message.chat.id]["vvod"] = True
    logging.info("запрос")
    resp = post(message.text, users[message.chat.id]["bot"])
    if resp.status_code == 200 and 'choices' in resp.json():
        if resp.json()['usage']['prompt_tokens'] < 100:
            gpt_response = resp.json()['choices'][0]['message']['content'] 
            users[message.chat.id]["vvod"] = False
            markup = nez()
            bot.send_message(message.chat.id, gpt_response, reply_markup=markup)
            logging.info("ответ получен")
            if users[message.chat.id]["debug"] == True:
                with open("log_file.txt", "rb") as f:
                    bot.send_document(message.chat.id, f)
            bot.register_next_step_handler(message, vyb)

        else:
            bot.send_message(message.chat.id, "Слишком большое количество токенов, сократи вопрос")
            logging.info("много токенов")
            if users[message.chat.id]["debug"] == True:
                with open("log_file.txt", "rb") as f:
                    bot.send_document(message.chat.id, f)
            bot.register_next_step_handler(message, gpt)

    else:
        bot.send_message(message.chat.id, resp.json())
        logging.warning("ошибка def gpt")
        if users[message.chat.id]["debug"] == True:
            with open("log_file.txt", "rb") as f:
                bot.send_document(message.chat.id, f)
def vyb(message):
    if message.text.lower() == 'завершить':
        bot.register_next_step_handler(message, vvod)
    elif message.text.lower() == 'продолжить':
        bot.register_next_step_handler(message, gpt)
    else:
        markup = nez()
        bot.send_message(message.chat.id, "попробуй ещё раз", reply_markup=markup)
        bot.register_next_step_handler(message, vyb)
def vybor(message):
    users[message.chat.id]["bot"] = boty[message.text]
    bot.send_message(message.chat.id, f"ты выбрал {message.text}")
    logging.info("смена режима бота")
    bot.register_next_step_handler(message, vvod)
bot.polling()