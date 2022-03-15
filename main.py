import logging
import sys
import os
import telegram
from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, ChosenInlineResultHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Update

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)


class MainBot:

    def __init__(self, token):
        self.token = token
        self.updater = Updater(self.token, use_context=True)
        self.dp = self.updater.dispatcher

        self.bot = telegram.Bot(self.token)
        self.reply_keyboard = [['Разделы'], ['Помощь', 'О боте']]
        self.markup = ReplyKeyboardMarkup(self.reply_keyboard, one_time_keyboard=False)

    def echo(self, update: Update, context: CallbackContext):
        # У объекта класса Updater есть поле message,
        # являющееся объектом сообщения.
        # У message есть поле text, содержащее текст полученного сообщения,
        # а также метод reply_text(str),
        # отсылающий ответ пользователю, от которого получено сообщение.
        update.message.reply_text(update.message.text)

    def start(self, update, context):
        update.message.reply_text(
            'Проверка_для_тестов',
            reply_markup=self.markup
        )

    def help(self, update, context):
        self.bot.sendMessage(chat_id=update.message.chat_id, text='GG')
        update.message.reply_text(
            'Это раздел помощь')

    def about_bot(self, update, context):
        update.message.reply_text(
            'Здесь будет текст о боте',
            reply_markup=self.markup
        )

    def sections(self, update, context):
        # список кнопок
        self.chat_id = update.message.chat_id
        button_list = [
            [InlineKeyboardButton("Физика(ЕГЭ)", callback_data='ФИЗИКА(ЕГЭ)')],
            [InlineKeyboardButton("Математика(олимпиады)", callback_data='МАТЕМАТИКА(олимпиады)')],
        ]
        # сборка клавиатуры из кнопок `InlineKeyboardButton`
        reply_markup = InlineKeyboardMarkup(button_list)
        # отправка клавиатуры в чат
        update.message.reply_text(text="Меню из двух столбцов", reply_markup=reply_markup)

    def choice(self, update, _):
        query = update.callback_query
        variant = query.data
        query.answer()
        # print(query.answer())
        # print(update)
        # редактируем сообщение, тем самым кнопки
        # в чате заменятся на этот ответ.
        query.edit_message_text(text=f'Выбран раздел: {variant}')
        if variant == 'ФИЗИКА(ЕГЭ)':
            print(update)
            work_class = Physics(self.token, self.bot, self.chat_id, update)
            work_class.main_physics()

    def main(self):
        self.dp.add_handler(MessageHandler(Filters.text('123'), self.echo))
        self.dp.add_handler(MessageHandler(Filters.text('Помощь'), self.help))
        # Регистрируем обработчик в диспетчере.
        self.dp.add_handler(CommandHandler('start', self.start))
        self.dp.add_handler(MessageHandler(Filters.text('О боте'), self.about_bot))
        self.dp.add_handler(MessageHandler(Filters.text('Разделы'), self.sections))
        self.dp.add_handler(CallbackQueryHandler(self.choice))
        # Запускаем цикл приема и обработки сообщений.
        self.updater.start_polling()

        # Ждём завершения приложения.
        self.updater.idle()


class Physics(MainBot):

    def __init__(self, token, bot, chat_id, update):
        super().__init__(token)
        self.bot = bot
        self.chat_id = chat_id
        self.update = update

    def main_physics(self):
        print('main_physics')
        # button_list = [
        #     [InlineKeyboardButton("Термодинамика", callback_data='ФИЗИКА(ЕГЭ)')],
        #     [InlineKeyboardButton("Математика(олимпиады)", callback_data='МАТЕМАТИКА(олимпиады)')],
        # ]
        # reply_markup = InlineKeyboardMarkup(button_list)
        # # отправка клавиатуры в чат
        # self.bot
        # self.bot.sendMessage.reply_text(text="Меню из двух столбцов", reply_markup=reply_markup)
        self.bot.sendMessage(chat_id=self.chat_id, text='GG')


if __name__ == '__main__':
    main_bot = MainBot('5136885850:AAFx-0jdcaXWeiY-0VObbXdFaECnQiku2nc')
    main_bot.main()
