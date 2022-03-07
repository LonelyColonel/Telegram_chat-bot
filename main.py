import logging
import sys
import os
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, ChosenInlineResultHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


class MainBot:

    def __init__(self, token):
        self.token = token
        self.updater = Updater(self.token, use_context=True)
        self.dp = self.updater.dispatcher
        self.reply_keyboard = [['Разделы'], ['Помощь', 'О боте']]
        self.markup = ReplyKeyboardMarkup(self.reply_keyboard, one_time_keyboard=False)

    def echo(self, update, context):
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
        update.message.reply_text(
            'Это раздел помощь')

    def about_bot(self, update, context):
        update.message.reply_text(
            'Здесь будет текст о боте',
            reply_markup=self.markup
        )

    def sections(self, update, context):
        # список кнопок
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
            # print(variant)
            # print(type(update))
            work_class = Physics(self.token)
            work_class.main_physics()
        # self.dp.add_handler(ChosenInlineResultHandler(variant), group=Physics.main_physics)


class Physics:
    def __init__(self, token):
        self.token = token
        self.updater = Updater(self.token, use_context=True)
        self.dp = self.updater.dispatcher
        # super().__init__(self)

    def oo(self, update, _):
        update.message.reply_text(text='физика_тестовый_принт')
    # def main_physics(self, update, _):
    #     update.message.reply_text(text='физика_тестовый_принт')

    def main_physics(self):
        self.dp.add_handler(MessageHandler(Filters.all(), self.oo))


def main():
    global reply_keyboard
    main_bot = MainBot('5136885850:AAFx-0jdcaXWeiY-0VObbXdFaECnQiku2nc')
    main_bot.dp.add_handler(MessageHandler(Filters.text('123'), main_bot.echo))
    main_bot.dp.add_handler(MessageHandler(Filters.text('Помощь'), main_bot.help))
    # Регистрируем обработчик в диспетчере.
    main_bot.dp.add_handler(CommandHandler('start', main_bot.start))
    main_bot.dp.add_handler(MessageHandler(Filters.text('О боте'), main_bot.about_bot))
    main_bot.dp.add_handler(MessageHandler(Filters.text('Разделы'), main_bot.sections))
    main_bot.dp.add_handler(CallbackQueryHandler(main_bot.choice))

    # Запускаем цикл приема и обработки сообщений.
    main_bot.updater.start_polling()

    # Ждём завершения приложения.
    main_bot.updater.idle()


if __name__ == '__main__':
    main()
