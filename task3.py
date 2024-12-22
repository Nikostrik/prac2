from telebot import types
from currency_converter import CurrencyConverter
import telebot

TOKEN = ""

bot = telebot.TeleBot(TOKEN)
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Вкажіть суму:')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Невірний формат. Вкажіть суму цифрами:')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Інше значення', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Виберіть валюту:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число від’ємне. Повторно вкажіть суму:')
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        try:
            res = currency.convert(amount, values[0], values[1])
            bot.send_message(call.message.chat.id, f'Отримуєте: {round(res, 2)}. Вкажіть іншу суму.')
            bot.register_next_step_handler(call.message, summa)
        except Exception:
            bot.send_message(call.message.chat.id, 'Помилка конвертації. Спробуйте ще раз.')
            bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Вкажіть свою конвертацію через слеш (наприклад, USD/EUR):')
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        if len(values) == 2:
            res = currency.convert(amount, values[0], values[1])
            bot.send_message(message.chat.id, f'Отримуєте: {round(res, 2)}. Можете вказати іншу суму:')
            bot.register_next_step_handler(message, summa)
        else:
            raise ValueError
    except Exception:
        bot.send_message(message.chat.id, 'Не вірне значення. Вкажіть суму повторно:')
        bot.register_next_step_handler(message, my_currency)

bot.polling(none_stop=True)

