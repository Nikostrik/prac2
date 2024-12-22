import wikipedia
import telebot

TOKEN = ""

bot = telebot.TeleBot(TOKEN)

def search_wikipedia(query):
    try:
        wikipedia.set_lang("uk")
        result = wikipedia.page(query)

        response = f"Назва статті: {result.title}\n\n"
        response += f"Основний текст статті: {result.summary}\n\n"
        response += f"Посилання на статтю: {result.url}"

        return response
    except wikipedia.exceptions.PageError:
        return "Сторінка не знайдена."


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Я Вікіпедія-Бот. Напишіть мені будь-який запит, і я знайду інформацію з Вікіпедії.")


@bot.message_handler(func=lambda message: True)
def handle_query(message):
    user_query = message.text
    response = search_wikipedia(user_query)
    bot.reply_to(message, response)

bot.polling()