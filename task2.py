import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


API = ""
TOKEN = ""

bot = telebot.TeleBot(TOKEN)

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric&lang=ua'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }
        return weather_info
    else:
        return None

@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Київ"), KeyboardButton("Львів"), KeyboardButton("Одеса"))
    bot.send_message(
        message.chat.id,
        "Вітаю! Я бот для прогнозу погоди. Введіть назву міста або оберіть місто зі списку нижче:",
        reply_markup=markup
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "Цей бот надає інформацію про погоду. Просто введіть назву міста або скористайтеся кнопками для швидкого вибору.\nКоманди:\n/start - Почати роботу з ботом\n/help - Отримати довідку"
    )

@bot.message_handler(content_types=['text'])
def get_weather_message(message):
    city = message.text.strip()
    weather = get_weather(city)
    if weather:
        response = (
            f"Погода в {city}:\n"
            f"Температура: {weather['temp']}°C\n"
            f"Опис: {weather['description'].capitalize()}\n"
            f"Швидкість вітру: {weather['wind_speed']} м/с"
        )
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "Не вдалося знайти місто. Спробуйте ще раз.")

bot.polling(none_stop=True)
