import telebot
from main import create
from download_upload import download_file, upload_file_to_file_io
import os


TOKEN = '8100535374:AAHFLQue5rL0u2DnHcV9MmcOzSN041HY3wM'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(user):
    bot.send_message(user.chat.id, 'Загрузите pdf файл по ссылке https://www.file.io/ и после отправьте полученную ссылку в бота')
    bot.send_message(user.chat.id,'По всем вопросам пишите Паше @ppppyzhkoff')


@bot.message_handler(content_types=['text'])
def handle_docs_photo(user):
    if user.text[0:5] == 'https':
        bot.send_message(user.chat.id, 'Ссылка получена. Файл скачивается.')
        try:
            downloaded_file = download_file(user.text)

            if downloaded_file:
                bot.send_message(user.chat.id, 'Файл скачан.')
                create(downloaded_file, bot, user.chat.id)
                bot.send_message(user.chat.id, 'Файл обработан и загружается, подождите...')
                upload_link = upload_file_to_file_io('Ценники.pdf')

                if upload_link:
                    bot.send_message(user.chat.id, f"Ссылка на файл: {upload_link}")
                else:
                    bot.send_message(user.chat.id, "Ошибка при загрузке файла. Пишите Паше")

                os.remove(downloaded_file)
                os.remove('Ценники.pdf')
            else:
                bot.send_message(user.chat.id, "Ошибка при скачивании файла. Пишите Паше")

        except Exception as e:
            bot.send_message(user.chat.id, f"Произошла ошибка: {str(e)}. Пишите Паше")


bot.polling(none_stop=True)
