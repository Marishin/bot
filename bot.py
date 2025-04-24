import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from os import getenv
from dotenv import load_dotenv
from random import randint

load_dotenv()
bot_token = getenv("TOKEN")

print(f"Токен из .env: {bot_token}")  # Должен вывести ваш токен
if not bot_token:
    print("❌ Токен не загружен!")


bot = telebot.TeleBot(bot_token)

# База слов
words_dict = {
    'apple': 'яблоко',
    'book': 'книга',
    'cat': 'кот',
    'dog': 'собака',
    'tree': 'дерево',
    'sun': 'солнце',
    'moon': 'луна',
    'car': 'машина',
    'pen': 'ручка',
    'chair': 'стул',
    'water': 'вода',
    'milk': 'молоко',
    'bird': 'птица',
    'table': 'стол',
    'ball': 'мяч',
    'hand': 'рука',
    'window': 'окно'
}

word_pairs = list(words_dict.items())

def send_word(message: Message):
    random4 = []
    while len(random4) < 4:
        new_pair = word_pairs[randint(0, len(word_pairs) - 1)]
        if new_pair not in random4:
            random4.append(new_pair)

    correct_pair = random4[randint(0, 3)]
    english_word = correct_pair[0]

    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for _, translation in random4:
        keyboard.add(KeyboardButton(translation))

    bot.send_message(
        chat_id=message.chat.id,
        text=f"Выбери перевод слова:\n👉 {english_word}",
        reply_markup=keyboard
    )

@bot.message_handler(commands=["start"])
def handle_start(message: Message):
    username = message.from_user.full_name or message.from_user.username
    welcome_text = f"""Привет, {username}! 👋

Я — бот для изучения английских слов. Давай потренируемся!

Готов? Тогда начнём. 👇"""
    bot.send_message(message.chat.id, welcome_text)
    send_word(message)

@bot.message_handler()
def handle_message(message: Message):
    print_info(message)
    bot.send_message(message.chat.id, "Спасибо за ответ! Попробуй ещё одно слово 😊")
    send_word(message)

def print_info(message: Message):
    info = f"""Вы написали: `{message.text}`
Пользователь: `{message.from_user.username}`
Чат ID: `{message.chat.id}`
"""
    print(info)
    bot.send_message(message.chat.id, info, parse_mode="Markdown")

bot.infinity_polling()