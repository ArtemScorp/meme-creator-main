import telebot, requests
import pyttsx3
from googletrans import Translator
import json
import os
import uuid

TOKEN = "8959021058:AAEPZ2Bipjz-kS2IzsClLp7GN_eN3PuHUeM"
bot = telebot.TeleBot(TOKEN)
# Инициализация синтезатора речи
engine = pyttsx3.init()  # Создаем объект для озвучивания текста



@bot.message_handler(commands=["start"])
def send_start(message):
    new = json.loads(get_news())
    text = new["text"]
    print(text)
    translator = Translator(service_urls=['translate.google.com'])
    result = translator.translate(text, dest='ru')
    print(result.text)

    bot.reply_to(message, result.text)

    audio_path = speak(result.text)
    with open(audio_path, 'rb') as audio:
        bot.send_audio(message.chat.id, audio)
    os.remove(audio_path)

def get_news() -> str:

    base_url = f"https://uselessfacts.jsph.pl/random.json"

    response = requests.get(base_url)

    # Проверяем, успешно ли выполнен запрос
    if response.status_code == 200:
        # Если все хорошо, возвращаем текст ответа
        return response.text.strip()
    else:
        # Если произошла ошибка, возвращаем сообщение об ошибке
        return "Не удалось получить данные. Попробуйте позже."


def speak(text: str) -> str:
    """
    Озвучивает текст и сохраняет его в аудиофайл для отправки через бота.
    
    Параметры:
        text (str): Текст для озвучивания
        
    Возвращает:
        str: Путь к созданному аудиофайлу (.wav)
    """
    filename = f"speech_{uuid.uuid4().hex}.wav"
    engine.save_to_file(text, filename)
    engine.runAndWait()
    return filename


# Запуск бота
bot.polling()  # Запускаем бесконечный цикл ожидания сообщений от пользователей
