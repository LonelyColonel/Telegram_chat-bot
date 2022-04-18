import logging
from telegram.ext import MessageHandler, Filters
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from main_class import MainBot
from data import db_session
from data.physics_tasks import PhysicsTasks
import json


# класс для физики (писал Миша)
class Physics(MainBot):
    def __init__(self, token, chat_id, dp, bot):
        super().__init__(token)
        self.bot = bot
        self.chat_id = chat_id
        self.dp = dp
        self.now_task = ''

    def main_physics(self):
        self.dp.add_handler(CallbackQueryHandler(self.physics_numbers, pattern='NUMBERS'))
        self.dp.add_handler(CallbackQueryHandler(self.physics_themes, pattern='THEMES'))
        button_list = [
            [InlineKeyboardButton("Номера", callback_data='NUMBERS')],
            [InlineKeyboardButton("Темы", callback_data='THEMES')]
        ]
        reply_markup = InlineKeyboardMarkup(button_list)
        self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup, text='Номера/Темы')

    def physics_themes(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.dp.add_handler(CallbackQueryHandler(self.meh, pattern='MEH'))
        self.dp.add_handler(CallbackQueryHandler(self.mkt, pattern='MKT'))
        self.dp.add_handler(CallbackQueryHandler(self.eld, pattern='EL'))
        self.dp.add_handler(CallbackQueryHandler(self.opt, pattern='OPT'))
        self.dp.add_handler(CallbackQueryHandler(self.kva, pattern='KV'))
        button_list = [
            [InlineKeyboardButton("Механика", callback_data='MEH')],
            [InlineKeyboardButton("МКТ и термодинамика", callback_data='MKT')],
            [InlineKeyboardButton("Электродинамика", callback_data='EL')],
            [InlineKeyboardButton("Оптика", callback_data='OPT')],
            [InlineKeyboardButton("Квантовая физика", callback_data='KV')],
        ]
        reply_markup = InlineKeyboardMarkup(button_list)
        self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup, text='Разделы')

    def physics_numbers(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        button_list = [[InlineKeyboardButton('1', callback_data='ONE'), InlineKeyboardButton('2', callback_data='TWO'),
                        InlineKeyboardButton('3', callback_data='THREE'),
                        InlineKeyboardButton('4', callback_data='FOUR'),
                        InlineKeyboardButton('5', callback_data='FIVE')],
                       [InlineKeyboardButton('6', callback_data='SIX'),
                        InlineKeyboardButton('7', callback_data='SEVEN'),
                        InlineKeyboardButton('8', callback_data='EIGHT'),
                        InlineKeyboardButton('9', callback_data='NINE'),
                        InlineKeyboardButton('10', callback_data='TEN')],
                       [InlineKeyboardButton('11', callback_data='ELEVEN'),
                        InlineKeyboardButton('12', callback_data='TWELVE'),
                        InlineKeyboardButton('13', callback_data='THIRTEEN'),
                        InlineKeyboardButton('14', callback_data='FOURTEEN'),
                        InlineKeyboardButton('15', callback_data='FIFTEEN')],
                       [InlineKeyboardButton('16', callback_data='SIXTEEN'),
                        InlineKeyboardButton('17', callback_data='SEVENTEEN'),
                        InlineKeyboardButton('18', callback_data='EIGHTEEN'),
                        InlineKeyboardButton('19', callback_data='NINETEEN'),
                        InlineKeyboardButton('20', callback_data='TWENTY')],
                       [InlineKeyboardButton('21', callback_data='TWONE'),
                        InlineKeyboardButton('22', callback_data='TWTWO'),
                        InlineKeyboardButton('23', callback_data='TWTHREE'),
                        InlineKeyboardButton('24', callback_data='TWFOUR'),
                        InlineKeyboardButton('25', callback_data='TWFIVE')],
                       [InlineKeyboardButton('26', callback_data='TWSIX'),
                        InlineKeyboardButton('27', callback_data='TWSEVEN'),
                        InlineKeyboardButton('28', callback_data='TWEIGHT'),
                        InlineKeyboardButton('29', callback_data='TWNINE'),
                        InlineKeyboardButton('30', callback_data='THIRTY')],
                       ]

        self.dp.add_handler(CallbackQueryHandler(self.one, pattern='ONE'))
        self.dp.add_handler(CallbackQueryHandler(self.two, pattern='TWO'))
        self.dp.add_handler(CallbackQueryHandler(self.three, pattern='THREE'))
        self.dp.add_handler(CallbackQueryHandler(self.four, pattern='FOUR'))
        self.dp.add_handler(CallbackQueryHandler(self.five, pattern='FIVE'))
        self.dp.add_handler(CallbackQueryHandler(self.six, pattern='SIX'))
        self.dp.add_handler(CallbackQueryHandler(self.seven, pattern='SEVEN'))
        self.dp.add_handler(CallbackQueryHandler(self.eight, pattern='EIGHT'))
        self.dp.add_handler(CallbackQueryHandler(self.nine, pattern='NINE'))
        self.dp.add_handler(CallbackQueryHandler(self.ten, pattern='TEN'))
        self.dp.add_handler(CallbackQueryHandler(self.eleven, pattern='ELEVEN'))
        self.dp.add_handler(CallbackQueryHandler(self.twelve, pattern='TWELVE'))
        self.dp.add_handler(CallbackQueryHandler(self.thirteen, pattern='THIRTEEN'))
        self.dp.add_handler(CallbackQueryHandler(self.fourteen, pattern='FOURTEEN'))
        self.dp.add_handler(CallbackQueryHandler(self.fifteen, pattern='FIFTEEN'))
        self.dp.add_handler(CallbackQueryHandler(self.sixteen, pattern='SIXTEEN'))
        self.dp.add_handler(CallbackQueryHandler(self.seventeen, pattern='SEVENTEEN'))
        self.dp.add_handler(CallbackQueryHandler(self.eighteen, pattern='EIGHTEEN'))
        self.dp.add_handler(CallbackQueryHandler(self.nineteen, pattern='NINETEEN'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty, pattern='TWENTY'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_one, pattern='TWONE'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_two, pattern='TWTWO'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_three, pattern='TWTHREE'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_four, pattern='TWFOUR'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_five, pattern='TWFIVE'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_six, pattern='TWSIX'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_seven, pattern='TWSEVEN'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_eight, pattern='TWEIGHT'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_nine, pattern='TWNINE'))
        self.dp.add_handler(CallbackQueryHandler(self.thirty, pattern='THIRTY'))
        reply_markup = InlineKeyboardMarkup(button_list)
        self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup, text='Номера')

    def meh(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = 'Mechanics'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, True)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def mkt(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = 'MKT and thermodynamics'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, True)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def eld(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = 'Electrodynamics'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, True)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def opt(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = 'Optics'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, True)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def kva(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = 'Quantum physics'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, True)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def one(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '1'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def two(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '2'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def three(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '3'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def four(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '4'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def five(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '5'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def six(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '6'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def seven(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '7'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def eight(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '8'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def nine(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '9'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def ten(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '10'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def eleven(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '11'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def twelve(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '12'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def thirteen(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '13'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def fourteen(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '14'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def fifteen(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '15'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def sixteen(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '16'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def seventeen(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '17'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def eighteen(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '18'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def nineteen(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '19'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def twenty(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '20'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def twenty_one(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '21'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def twenty_two(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '22'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def twenty_three(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '23'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def twenty_four(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '24'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def twenty_five(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '25'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def twenty_six(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '26'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def twenty_seven(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '27'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def twenty_eight(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '28'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def twenty_nine(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '29'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def thirty(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        self.now_task = '30'
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        self.db_task = self.open_document(session, self.now_task, False)
        if self.db_task == '-END-':
            self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
        else:
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].way_physics, 'rb'))
            self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
            self.dp.add_handler(MessageHandler(Filters.text, self.answer_check), group=1)

    def open_document(self, session, them, is_them):
        with open('Json_data/' + str(self.chat_id) + '.json') as file:
            data = json.load(file)
        if data[0][them][0]['lvl'] < 5:
            dif = 'Л'
        elif 10 > data[0][them][0]['lvl'] > 5:
            dif = 'С'
        else:
            dif = 'Т'
        tasks_list = []
        if is_them:
            for i in session.query(PhysicsTasks).filter(PhysicsTasks.theme_physics == f'{them}',
                                                        PhysicsTasks.id_physics_tasks.notin_(data[0]['completed']),
                                                        PhysicsTasks.id_physics_tasks.notin_(data[0]['failed']),
                                                        PhysicsTasks.difficulty_physics == dif):
                tasks_list.append(i)
            if not tasks_list:
                for i in session.query(PhysicsTasks).filter(PhysicsTasks.theme_physics == f'{them}',
                                                            PhysicsTasks.id_physics_tasks.notin_(data[0]['completed']),
                                                            PhysicsTasks.difficulty_physics == dif):
                    tasks_list.append(i)
                if not tasks_list:
                    if dif == 'Т':
                        for i in session.query(PhysicsTasks).filter(PhysicsTasks.theme_physics == f'{them}',
                                                                    PhysicsTasks.id_physics_tasks.notin_(
                                                                        data[0]['completed']),
                                                                    PhysicsTasks.id_physics_tasks.notin_(
                                                                        data[0]['failed']),
                                                                    PhysicsTasks.difficulty_physics == 'С'):
                            tasks_list.append(i)
                        if not tasks_list:
                            for i in session.query(PhysicsTasks).filter(PhysicsTasks.theme_physics == f'{them}',
                                                                        PhysicsTasks.id_physics_tasks.notin_(
                                                                            data[0]['completed']),
                                                                        PhysicsTasks.difficulty_physics == 'С'):
                                tasks_list.append(i)
                                if not tasks_list:
                                    for i in session.query(PhysicsTasks).filter(PhysicsTasks.theme_physics == f'{them}',
                                                                                PhysicsTasks.id_physics_tasks.notin_(
                                                                                    data[0]['completed']),
                                                                                PhysicsTasks.id_physics_tasks.notin_(
                                                                                    data[0]['failed']),
                                                                                PhysicsTasks.difficulty_physics == 'Л'):
                                        tasks_list.append(i)
                                        if not tasks_list:
                                            for i in session.query(PhysicsTasks).filter(
                                                    PhysicsTasks.theme_physics == f'{them}',
                                                    PhysicsTasks.id_physics_tasks.notin_(
                                                        data[0]['completed']),
                                                    PhysicsTasks.difficulty_physics == 'Л'):
                                                tasks_list.append(i)
                                            if not tasks_list:
                                                file.close()
                                                return '-END-'
                    elif dif == 'С':
                        for i in session.query(PhysicsTasks).filter(PhysicsTasks.theme_physics == f'{them}',
                                                                    PhysicsTasks.id_physics_tasks.notin_(
                                                                        data[0]['completed']),
                                                                    PhysicsTasks.id_physics_tasks.notin_(
                                                                        data[0]['failed']),
                                                                    PhysicsTasks.difficulty_physics == 'Л'):
                            tasks_list.append(i)
                            if not tasks_list:
                                for i in session.query(PhysicsTasks).filter(
                                        PhysicsTasks.theme_physics == f'{them}',
                                        PhysicsTasks.id_physics_tasks.notin_(
                                            data[0]['completed']),
                                        PhysicsTasks.difficulty_physics == 'Л'):
                                    tasks_list.append(i)
                                if not tasks_list:
                                    file.close()
                                    return '-END-'
                    else:
                        file.close()
                        return '-END-'
        else:
            for i in session.query(PhysicsTasks).filter(PhysicsTasks.number_physics == f'{them}',
                                                        PhysicsTasks.id_physics_tasks.notin_(data[0]['completed']),
                                                        PhysicsTasks.id_physics_tasks.notin_(data[0]['failed']),
                                                        PhysicsTasks.difficulty_physics == dif):
                tasks_list.append(i)
            if not tasks_list:
                for i in session.query(PhysicsTasks).filter(PhysicsTasks.number_physics == f'{them}',
                                                            PhysicsTasks.id_physics_tasks.notin_(data[0]['completed']),
                                                            PhysicsTasks.difficulty_physics == dif):
                    tasks_list.append(i)
                if not tasks_list:
                    if dif == 'Т':
                        for i in session.query(PhysicsTasks).filter(PhysicsTasks.number_physics == f'{them}',
                                                                    PhysicsTasks.id_physics_tasks.notin_(
                                                                        data[0]['completed']),
                                                                    PhysicsTasks.id_physics_tasks.notin_(
                                                                        data[0]['failed']),
                                                                    PhysicsTasks.difficulty_physics == 'С'):
                            tasks_list.append(i)
                        if not tasks_list:
                            for i in session.query(PhysicsTasks).filter(PhysicsTasks.number_physics == f'{them}',
                                                                        PhysicsTasks.id_physics_tasks.notin_(
                                                                            data[0]['completed']),
                                                                        PhysicsTasks.difficulty_physics == 'С'):
                                tasks_list.append(i)
                                if not tasks_list:
                                    for i in session.query(PhysicsTasks).filter(PhysicsTasks.themnumber_physicse_physics
                                                                                == f'{them}',
                                                                                PhysicsTasks.id_physics_tasks.notin_(
                                                                                    data[0]['completed']),
                                                                                PhysicsTasks.id_physics_tasks.notin_(
                                                                                    data[0]['failed']),
                                                                                PhysicsTasks.difficulty_physics == 'Л'):
                                        tasks_list.append(i)
                                        if not tasks_list:
                                            for i in session.query(PhysicsTasks).filter(
                                                    PhysicsTasks.number_physics == f'{them}',
                                                    PhysicsTasks.id_physics_tasks.notin_(
                                                        data[0]['completed']),
                                                    PhysicsTasks.difficulty_physics == 'Л'):
                                                tasks_list.append(i)
                                            if not tasks_list:
                                                file.close()
                                                return '-END-'
                    elif dif == 'С':
                        for i in session.query(PhysicsTasks).filter(PhysicsTasks.number_physics == f'{them}',
                                                                    PhysicsTasks.id_physics_tasks.notin_(
                                                                        data[0]['completed']),
                                                                    PhysicsTasks.id_physics_tasks.notin_(
                                                                        data[0]['failed']),
                                                                    PhysicsTasks.difficulty_physics == 'Л'):
                            tasks_list.append(i)
                            if not tasks_list:
                                for i in session.query(PhysicsTasks).filter(
                                        PhysicsTasks.number_physics == f'{them}',
                                        PhysicsTasks.id_physics_tasks.notin_(
                                            data[0]['completed']),
                                        PhysicsTasks.difficulty_physics == 'Л'):
                                    tasks_list.append(i)
                                if not tasks_list:
                                    file.close()
                                    return '-END-'
                    else:
                        file.close()
                        return '-END-'
        file.close()
        return tasks_list

    def answer_check(self, update, _):
        self.chat_id = update.message.chat_id
        answer = update.message.text
        self.dp.handlers[1].clear()
        if answer in ['Разделы', 'Помощь/О боте', 'Обратная связь']:
            return
        with open('Json_data/' + str(self.chat_id) + '.json') as file:
            data = json.load(file)
        if answer == self.db_task[0].answer_physics:
            data[0]['completed'].append(int(self.db_task[0].id_physics_tasks))
            if int(self.db_task[0].id_physics_tasks) in data[0]['failed']:
                data[0]['failed'].remove(int(self.db_task[0].id_physics_tasks))
            data[0][self.now_task][0]['lvl'] += 1
            self.bot.sendMessage(chat_id=self.chat_id, text='Ответ правильный!')
        else:
            data[0]['failed'].append(int(self.db_task[0].id_physics_tasks))
            self.bot.sendMessage(chat_id=self.chat_id, text='Ответ неправильный!')
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.db_task[0].solution_physics, 'rb'))
        file.close()
        with open('Json_data/' + str(self.chat_id) + '.json', mode='w') as file:
            json.dump(data, file)
            file.close()
        self.db_task.clear()

