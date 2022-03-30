import logging
import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, ChosenInlineResultHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from main_class import MainBot


class Physics(MainBot):
    def __init__(self, token, bot, chat_id, dp):
        super().__init__(token)
        self.bot = bot
        self.chat_id = chat_id
        self.dp = dp

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
        self.dp.add_handler(CallbackQueryHandler(self.one, pattern='1T'))
        self.dp.add_handler(CallbackQueryHandler(self.two, pattern='2T'))
        self.dp.add_handler(CallbackQueryHandler(self.three, pattern='3T'))
        self.dp.add_handler(CallbackQueryHandler(self.four, pattern='4T'))
        self.dp.add_handler(CallbackQueryHandler(self.five, pattern='5T'))
        self.dp.add_handler(CallbackQueryHandler(self.six, pattern='6T'))
        self.dp.add_handler(CallbackQueryHandler(self.seven, pattern='7T'))
        self.dp.add_handler(CallbackQueryHandler(self.eight, pattern='8T'))
        self.dp.add_handler(CallbackQueryHandler(self.nine, pattern='9T'))
        self.dp.add_handler(CallbackQueryHandler(self.ten, pattern='10T'))
        self.dp.add_handler(CallbackQueryHandler(self.eleven, pattern='11T'))
        self.dp.add_handler(CallbackQueryHandler(self.twelve, pattern='12T'))
        self.dp.add_handler(CallbackQueryHandler(self.thirteen, pattern='13T'))
        self.dp.add_handler(CallbackQueryHandler(self.fourteen, pattern='14T'))
        self.dp.add_handler(CallbackQueryHandler(self.fifteen, pattern='15T'))
        self.dp.add_handler(CallbackQueryHandler(self.sixteen, pattern='16T'))
        self.dp.add_handler(CallbackQueryHandler(self.seventeen, pattern='17T'))
        self.dp.add_handler(CallbackQueryHandler(self.eighteen, pattern='18T'))
        self.dp.add_handler(CallbackQueryHandler(self.nineteen, pattern='19T'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty, pattern='20T'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_one, pattern='21T'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_two, pattern='22T'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_three, pattern='23T'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_four, pattern='24T'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_five, pattern='25T'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_six, pattern='26T'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_seven, pattern='27T'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_eight, pattern='28T'))
        self.dp.add_handler(CallbackQueryHandler(self.twenty_nine, pattern='29T'))
        self.dp.add_handler(CallbackQueryHandler(self.thirty, pattern='30T'))
        button_list = [[InlineKeyboardButton('1', callback_data='1T'), InlineKeyboardButton('2', callback_data='2T'),
                        InlineKeyboardButton('3', callback_data='3T'), InlineKeyboardButton('4', callback_data='4T'),
                        InlineKeyboardButton('5', callback_data='5T')],
                       [InlineKeyboardButton('6', callback_data='6T'), InlineKeyboardButton('7', callback_data='7T'),
                        InlineKeyboardButton('8', callback_data='8T'), InlineKeyboardButton('9', callback_data='9T'),
                        InlineKeyboardButton('10', callback_data='10T')],
                       [InlineKeyboardButton('11', callback_data='11T'), InlineKeyboardButton('12', callback_data='12T'),
                        InlineKeyboardButton('13', callback_data='13T'), InlineKeyboardButton('14', callback_data='14T'),
                        InlineKeyboardButton('15', callback_data='15T')],
                       [InlineKeyboardButton('16', callback_data='16T'), InlineKeyboardButton('17', callback_data='17T'),
                        InlineKeyboardButton('18', callback_data='18T'), InlineKeyboardButton('19', callback_data='19T'),
                        InlineKeyboardButton('20', callback_data='20T')],
                       [InlineKeyboardButton('21', callback_data='21T'), InlineKeyboardButton('22', callback_data='22T'),
                        InlineKeyboardButton('23', callback_data='23T'), InlineKeyboardButton('24', callback_data='24T'),
                        InlineKeyboardButton('25', callback_data='25T')],
                       [InlineKeyboardButton('26', callback_data='26T'), InlineKeyboardButton('27', callback_data='27T'),
                        InlineKeyboardButton('28', callback_data='28T'), InlineKeyboardButton('29', callback_data='29T'),
                        InlineKeyboardButton('30', callback_data='30T')],
                       ]
        reply_markup = InlineKeyboardMarkup(button_list)
        self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup, text='Номера')

    def meh(self, update, _):
        pass

    def mkt(self, update, _):
        pass

    def eld(self, update, _):
        pass

    def opt(self, update, _):
        pass

    def kva(self, update, _):
        pass

    def one(self, update, _):
        pass

    def two(self, update, _):
        pass

    def three(self, update, _):
        pass

    def four(self, update, _):
        pass

    def five(self, update, _):
        pass

    def six(self, update, _):
        pass

    def seven(self, update, _):
        pass

    def eight(self, update, _):
        pass

    def nine(self, update, _):
        pass

    def ten(self, update, _):
        pass

    def eleven(self, update, _):
        pass

    def twelve(self, update, _):
        pass

    def thirteen(self, update, _):
        pass

    def fourteen(self, update, _):
        pass

    def fifteen(self, update, _):
        pass

    def sixteen(self, update, _):
        pass

    def seventeen(self, update, _):
        pass

    def eighteen(self, update, _):
        pass

    def nineteen(self, update, _):
        pass

    def twenty(self, update, _):
        pass

    def twenty_one(self, update, _):
        pass

    def twenty_two(self, update, _):
        pass

    def twenty_three(self, update, _):
        pass

    def twenty_four(self, update, _):
        pass

    def twenty_five(self, update, _):
        pass

    def twenty_six(self, update, _):
        pass

    def twenty_seven(self, update, _):
        pass

    def twenty_eight(self, update, _):
        pass

    def twenty_nine(self, update, _):
        pass

    def thirty(self, update, _):
        pass
