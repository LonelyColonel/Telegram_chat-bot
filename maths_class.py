import logging
import json
from telegram.ext import MessageHandler, Filters
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from main_class import MainBot
from data import db_session
from data.maths_tasks import MathsTasks
from maths_dictionaries import global_slovar, slovar, slovar_names


class Maths(MainBot):
    def __init__(self, token, bot, chat_id, dp):
        super().__init__(token)
        self.bot = bot
        self.chat_id = chat_id
        self.dp = dp
        self.global_slovar = global_slovar
        self.slovar = slovar
        self.slovar_names = slovar_names
        self.spisok_tasks = []
        self.current_task = ''

    def main_maths(self):
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='-TRIGONOMETRY-'))
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='-EQUATIONS-'))
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='-SYSTEM-'))
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='-TEXT_TASKS-'))
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='-PARAMETERS-'))
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='-PLANIMETRY-'))
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='-STEREOMETRY-'))
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='-OTHER_VAR-'))
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='-NON_STANDART-'))
        self.themes_maths()

    def themes_maths(self):
        button_list = [
            [InlineKeyboardButton("Тригонометрия", callback_data='-TRIGONOMETRY-')],
            [InlineKeyboardButton("Уравнения и неравенства", callback_data='-EQUATIONS-')],
            [InlineKeyboardButton("Алгебраические системы", callback_data='-SYSTEM-')],
            [InlineKeyboardButton("Текстовые задачи", callback_data='-TEXT_TASKS-')],
            [InlineKeyboardButton("Параметры", callback_data='-PARAMETERS-')],
            [InlineKeyboardButton("Планиметрия", callback_data='-PLANIMETRY-')],
            [InlineKeyboardButton("Стереометрия", callback_data='-STEREOMETRY-')],
            [InlineKeyboardButton("Из вариантов олимпиад прошлых лет", callback_data='-OTHER_VAR-')],
            [InlineKeyboardButton("Нестандартные задачи", callback_data='-NON_STANDART-')]
        ]
        reply_markup = InlineKeyboardMarkup(button_list)
        self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup, text='Темы')

    def common_handler_function(self, update, _):
        query = update.callback_query
        variant = query.data
        query.answer()
        query.delete_message()

        theme_for_text = self.slovar_names[variant]
        trig_btns = self.global_slovar[f'{theme_for_text}']

        reply_markup = InlineKeyboardMarkup(trig_btns)
        if theme_for_text in ['Текстовые задачи', 'Параметры', 'Планиметрия', 'Стереометрия',
                              'Из вариантов олимпиад прошлых лет', 'Нестандартные задачи']:
            self.bot.sendMessage(chat_id=self.chat_id, text='Данный раздел находится в разработке!')
        else:
            self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                                 text=f'Тема: {theme_for_text}. Выберите подтемы:')

        theme = self.slovar[variant]
        for i in theme:
            self.dp.add_handler(CallbackQueryHandler(self.for_send_tasks, pattern=f'{i}'))

    def for_send_tasks(self, update, _):
        query = update.callback_query
        variant = query.data
        query.answer()
        query.delete_message()
        print(variant)
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        # self.spisok_tasks = []
        with open('Json_data/' + str(self.chat_id) + '.json') as file:
            data = json.load(file)
        for i in session.query(MathsTasks).filter(MathsTasks.undertheme_maths == f'{variant}',
                                                  MathsTasks.id_maths_tasks.notin_(data[1]['completed_maths']),
                                                  MathsTasks.id_maths_tasks.notin_(data[1]['failed_maths'])):
            self.spisok_tasks.append(str(i).split())
        if not self.spisok_tasks:
            for i in session.query(MathsTasks).filter(MathsTasks.undertheme_maths == f'{variant}',
                                                      MathsTasks.id_maths_tasks.notin_(data[1]['completed_maths'])):
                self.spisok_tasks.append(str(i).split())
            if not self.spisok_tasks:
                self.bot.sendMessage(chat_id=self.chat_id, text='Новых заданий больше нет!')
                return
        self.bot.sendDocument(chat_id=self.chat_id, document=open(self.spisok_tasks[0][5], 'rb'))
        self.bot.sendMessage(chat_id=self.chat_id, text='Отправьте ответ')
        self.dp.add_handler(MessageHandler(Filters.text, self.answer_handler), group=1)

    def answer_handler(self, update, _):
        answer = update.message.text
        if answer in ['Разделы', 'Помощь/О боте', 'Обратная связь']:
            self.dp.handlers[1].clear()
            return
        self.current_task = self.spisok_tasks[0][1]
        if answer == self.spisok_tasks[0][6]:
            with open('Json_data/' + str(self.chat_id) + '.json') as file:
                data = json.load(file)
                data[1]['completed_maths'].append(int(self.spisok_tasks[0][1]))
                if int(self.spisok_tasks[0][1]) in data[1]['failed_maths']:
                    data[1]['failed_maths'].remove(int(self.spisok_tasks[0][1]))
                file.close()
            self.bot.sendMessage(chat_id=self.chat_id, text='Ответ правильный!')
        else:
            with open('Json_data/' + str(self.chat_id) + '.json') as file:
                data = json.load(file)
                data[1]['failed_maths'].append(int(self.spisok_tasks[0][1]))
                file.close()
            self.bot.sendMessage(chat_id=self.chat_id, text='Ответ неправильный!')
            self.bot.sendDocument(chat_id=self.chat_id, document=open(self.spisok_tasks[0][7], 'rb'))
            btn = [[InlineKeyboardButton('Я прав', callback_data='I_BATYA')]]
            self.dp.add_handler(CallbackQueryHandler(self.true_answer, pattern='I_BATYA'))
            reply_markup = InlineKeyboardMarkup(btn)
            self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup, text='Нажмите на кнопку под этим '
                                                                                       'сообщением, если ваш '
                                                                                       'ответ верный, но вы '
                                                                                       'неправильно его ввели.')
        with open('Json_data/' + str(self.chat_id) + '.json', mode='w') as file:
            json.dump(data, file)
            file.close()
        self.spisok_tasks.clear()

    def true_answer(self, update, _):
        update.callback_query.delete_message()
        with open('Json_data/' + str(self.chat_id) + '.json') as file:
            data = json.load(file)
            data[1]['failed_maths'].pop(-1)
            data[1]['completed_maths'].append(int(self.current_task))
        with open('Json_data/' + str(self.chat_id) + '.json', mode='w') as file:
            json.dump(data, file)
            file.close()
        self.bot.sendMessage(chat_id=self.chat_id, text='Хорошо, задача засчитана как правильно решённая')
