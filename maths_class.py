import logging
import telegram
import sqlalchemy
import json
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, ChosenInlineResultHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from main_class import MainBot
from data import db_session
from data.maths_tasks import MathsTasks
from data.users import BotUser


global_spisok_names = ['Тригонометрия', 'Уравнения и неравенства', 'Алгебраические системы', 'Текстовые задачи',
                       'Параметры', 'Планиметрия', 'Стереометрия', 'Из вариантов олимпиад прошлых лет',
                       'Нестандартные задачи']

global_slovar = {'Тригонометрия': [
                              [InlineKeyboardButton("Триг. ур-ия", callback_data='TRIGONOMETRY_EQUATIONS')],
                              [InlineKeyboardButton("Сведение к кв-ым триг. ур-ям",
                                                    callback_data='SQUARE_EQUATIONS')],
                              [InlineKeyboardButton("Однородные ур-ия", callback_data='SINGLE_TRIGONOMETRY')],
                              [InlineKeyboardButton("Системы триг. уравнений", callback_data='TRIGONOMETRY_SYSTEM')],
                              [InlineKeyboardButton("Преобразование триг. уравнений",
                                                    callback_data='TRANSFORMATIONS')],
                              [InlineKeyboardButton("Обратные триг. функции", callback_data='INVERSE_FUNCTIONS')],
                              [InlineKeyboardButton("Метод вспомогательного угла в триг.",
                                                    callback_data='SUPPORT_ANGLE')]],
                 'Уравнения и неравенства': [
                              [InlineKeyboardButton("Уравнения и неравенства с модулем", callback_data='EQUATIONS')],
                              [InlineKeyboardButton("Рациональные уравнения и неравенства",
                                                    callback_data='SQUARE_EQUATIONS')],
                              [InlineKeyboardButton("Уравнения и неравенства с радикалами",
                                                    callback_data='SINGLE_TRIGONOMETRY')],
                              [InlineKeyboardButton("Показательные уравнения", callback_data='TRIGONOMETRY_SYSTEM')],
                              [InlineKeyboardButton("Логарифмические уравнения",
                                                    callback_data='TRANSFORMATIONS')],
                              [InlineKeyboardButton("Смешанная тригонометрия", callback_data='INVERSE_FUNCTIONS')],
                              [InlineKeyboardButton("Смешанные уравнения",
                                                    callback_data='SUPPORT_ANGLE')]],
                 'Алгебраические системы': [
                              [InlineKeyboardButton("Простые системы уравнений",
                                                    callback_data='TRIGONOMETRY_EQUATIONS')],
                              [InlineKeyboardButton("Сложные системы уравнений",
                                                    callback_data='SQUARE_EQUATIONS')],
                              [InlineKeyboardButton("Возникающие из текстовых задач",
                                                    callback_data='SINGLE_TRIGONOMETRY')]],

                 'Текстовые задачи': [
                              [InlineKeyboardButton("Задачи на движение", callback_data='TRIGONOMETRY_EQUATIONS')],
                              [InlineKeyboardButton("Задачи на работу",
                                                    callback_data='SQUARE_EQUATIONS')],
                              [InlineKeyboardButton("Задачи на смеси", callback_data='SINGLE_TRIGONOMETRY')],
                              [InlineKeyboardButton("Задачи на прогрессии", callback_data='TRIGONOMETRY_SYSTEM')],
                              [InlineKeyboardButton("Оптимальный выбор и целые числа",
                                                    callback_data='TRANSFORMATIONS')]],

                 'Параметры': [
                              [InlineKeyboardButton("Квадратные ур-ия и нер-ва с параметром",
                                                    callback_data='TRIGONOMETRY_EQUATIONS')],
                              [InlineKeyboardButton("Логические задачи",
                                                    callback_data='SQUARE_EQUATIONS')],
                              [InlineKeyboardButton("Сложные логические задачи", callback_data='SINGLE_TRIGONOMETRY')],
                              [InlineKeyboardButton("Параметры с корнями", callback_data='TRIGONOMETRY_SYSTEM')]],

                 'Планиметрия': [
                              [InlineKeyboardButton("Общие треугольники", callback_data='TRIGONOMETRY_EQUATIONS')],
                              [InlineKeyboardButton("Подобие",
                                                    callback_data='SQUARE_EQUATIONS')],
                              [InlineKeyboardButton("Площади", callback_data='SINGLE_TRIGONOMETRY')],
                              [InlineKeyboardButton("Параллелограммы и трапеции", callback_data='TRIGONOMETRY_SYSTEM')],
                              [InlineKeyboardButton("Окружности",
                                                    callback_data='TRANSFORMATIONS')],
                              [InlineKeyboardButton("Построения", callback_data='INVERSE_FUNCTIONS')]],

                 'Стереометрия': [
                              [InlineKeyboardButton("Триг. ур-ия", callback_data='TRIGONOMETRY_EQUATIONS')],
                              [InlineKeyboardButton("Сведение к кв-ым триг. ур-ям",
                                                    callback_data='SQUARE_EQUATIONS')],
                              [InlineKeyboardButton("Однородные ур-ия", callback_data='SINGLE_TRIGONOMETRY')],
                              [InlineKeyboardButton("Системы триг. уравнений", callback_data='TRIGONOMETRY_SYSTEM')],
                              [InlineKeyboardButton("Преобразование триг. уравнений",
                                                    callback_data='TRANSFORMATIONS')],
                              [InlineKeyboardButton("Обратные триг. функции", callback_data='INVERSE_FUNCTIONS')],
                              [InlineKeyboardButton("Метод вспомогательного угла в триг.",
                                                    callback_data='SUPPORT_ANGLE')]],
                 'Из вариантов олимпиад прошлых лет': [
                              [InlineKeyboardButton("Физтех", callback_data='TRIGONOMETRY_EQUATIONS')],
                              [InlineKeyboardButton("ОММО",
                                                    callback_data='SQUARE_EQUATIONS')],
                              [InlineKeyboardButton("ПВГ", callback_data='SINGLE_TRIGONOMETRY')],
                              [InlineKeyboardButton("Ломоносов", callback_data='TRIGONOMETRY_SYSTEM')],
                              [InlineKeyboardButton("Росатом",
                                                    callback_data='TRANSFORMATIONS')],
                              [InlineKeyboardButton("САММАТ", callback_data='INVERSE_FUNCTIONS')],
                              [InlineKeyboardButton("Газпром",
                                                    callback_data='SUPPORT_ANGLE')]],

                 'Нестандартные задачи': [
                              [InlineKeyboardButton("Метод мажорант", callback_data='TRIGONOMETRY_EQUATIONS')],
                              [InlineKeyboardButton("Использование св-в функций",
                                                    callback_data='SQUARE_EQUATIONS')],
                              [InlineKeyboardButton("Подстановка или группировка", callback_data='SINGLE_TRIGONOMETRY')],
                              [InlineKeyboardButton("Геометрический подход", callback_data='TRIGONOMETRY_SYSTEM')]],

                 }


class Maths(MainBot):
    def __init__(self, token, bot, chat_id, dp):
        super().__init__(token)
        self.bot = bot
        self.chat_id = chat_id
        self.dp = dp
        self.WAY = ''
        self.global_slovar = global_slovar
        self.spisok_tasks = []

    def main_maths(self):
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='-TRIGONOMETRY-'))
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='EQUATIONS'))
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='SYSTEM'))
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='TEXT_TASKS'))
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='PARAMETERS'))
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='PLANIMETRY'))
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='STEREOMETRY'))
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='OTHER_VAR'))
        self.dp.add_handler(CallbackQueryHandler(self.common_handler_function, pattern='NON_STANDART'))
        self.themes_maths()

    def themes_maths(self):
        button_list = [
            [InlineKeyboardButton("Тригонометрия", callback_data='-TRIGONOMETRY-')],
            [InlineKeyboardButton("Уравнения и неравенства", callback_data='EQUATIONS')],
            [InlineKeyboardButton("Алгебраические системы", callback_data='SYSTEM')],
            [InlineKeyboardButton("Текстовые задачи", callback_data='TEXT_TASKS')],
            [InlineKeyboardButton("Параметры", callback_data='PARAMETERS')],
            [InlineKeyboardButton("Планиметрия", callback_data='PLANIMETRY')],
            [InlineKeyboardButton("Стереометрия", callback_data='STEREOMETRY')],
            [InlineKeyboardButton("Из вариантов олимпиад прошлых лет", callback_data='OTHER_VAR')],
            [InlineKeyboardButton("Нестандартные задачи", callback_data='NON_STANDART')]
        ]
        reply_markup = InlineKeyboardMarkup(button_list)
        self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup, text='Темы')

    def common_handler_function(self, update, _):
        query = update.callback_query
        variant = query.data
        query.answer()
        query.delete_message()
        self.WAY += variant                                 # TODO: не забыть прописать переменную WAY во всех подтемах
        if variant == '-TRIGONOMETRY-':
            # self.trigonometry()
            trig_btns = self.global_slovar['Тригонометрия']

            reply_markup = InlineKeyboardMarkup(trig_btns)
            self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                                 text='Тема: ТРИГОНОМЕТРИЯ. Выберите подтемы:')
            self.dp.add_handler(CallbackQueryHandler(self.trigonometry, pattern='TRIGONOMETRY_EQUATIONS'))
            self.dp.add_handler(CallbackQueryHandler(self.trigonometry, pattern='SQUARE_EQUATIONS'))
            self.dp.add_handler(CallbackQueryHandler(self.trigonometry, pattern='SINGLE_TRIGONOMETRY'))
            self.dp.add_handler(CallbackQueryHandler(self.trigonometry, pattern='TRIGONOMETRY_SYSTEM'))
            self.dp.add_handler(CallbackQueryHandler(self.trigonometry, pattern='TRANSFORMATIONS'))
            self.dp.add_handler(CallbackQueryHandler(self.trigonometry, pattern='INVERSE_FUNCTIONS'))
            self.dp.add_handler(CallbackQueryHandler(self.trigonometry, pattern='SUPPORT_ANGLE'))

        elif variant == 'EQUATIONS':
            # self.equations()
            equations_btns = self.global_slovar['Уравнения и неравенства']

            reply_markup = InlineKeyboardMarkup(equations_btns)
            self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                                 text='Тема: Уравнения и неравенства. Выберите подтемы:')
        elif variant == 'SYSTEM':
            # self.systems()
            systems_btns = self.global_slovar['Алгебраические системы']

            reply_markup = InlineKeyboardMarkup(systems_btns)
            self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                                 text='Тема: ТРИГОНОМЕТРИЯ. Выберите подтемы:')
        elif variant == 'TEXT_TASKS':
            # self.text_tasks()
            text_tasks_btns = self.global_slovar['Текстовые задачи']

            reply_markup = InlineKeyboardMarkup(text_tasks_btns)
            self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                                 text='Тема: ТРИГОНОМЕТРИЯ. Выберите подтемы:')
        elif variant == 'PARAMETERS':
            # self.parameters()
            parameters_btns = self.global_slovar['Параметры']

            reply_markup = InlineKeyboardMarkup(parameters_btns)
            self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                                 text='Тема: ТРИГОНОМЕТРИЯ. Выберите подтемы:')

        elif variant == 'PLANIMETRY':
            # self.planimetry()
            planimetry_btns = self.global_slovar['Планиметрия']

            reply_markup = InlineKeyboardMarkup(planimetry_btns)
            self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                                 text='Тема: ТРИГОНОМЕТРИЯ. Выберите подтемы:')

        elif variant == 'STEREOMETRY':
            # self.stereometry()
            stereometry_btns = self.global_slovar['Стереометрия']

            reply_markup = InlineKeyboardMarkup(stereometry_btns)
            self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                                 text='Тема: ТРИГОНОМЕТРИЯ. Выберите подтемы:')
        elif variant == 'OTHER_VAR':
            # self.other_var()
            other_var_btns = self.global_slovar['Из вариантов олимпиад прошлых лет']

            reply_markup = InlineKeyboardMarkup(other_var_btns)
            self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                                 text='Тема: ТРИГОНОМЕТРИЯ. Выберите подтемы:')
        elif variant == 'NON_STANDART':
            # self.non_standart()
            non_standart_btns = self.global_slovar['Нестандартные задачи']

            reply_markup = InlineKeyboardMarkup(non_standart_btns)
            self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                                 text='Тема: ТРИГОНОМЕТРИЯ. Выберите подтемы:')

    def trigonometry(self, update, _):
        query = update.callback_query
        variant = query.data
        query.answer()
        query.delete_message()
        # if variant == 'TRIGONOMETRY_EQUATIONS':
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        # self.spisok_tasks = []
        with open('Json_data/' + str(self.chat_id) + '.json') as file:
            data = json.load(file)
        for i in session.query(MathsTasks).filter(MathsTasks.undertheme_maths == f'{variant}',
                                                  MathsTasks.id_maths_tasks.notin_(data[1]['completed_maths']),
                                                  MathsTasks.id_maths_tasks.notin_(data[1]['failed_maths'])):
            self.spisok_tasks.append(str(i).split())
        print(self.spisok_tasks)
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
        # W - решена, F - решена неправильно, N - не решалась
        answer = update.message.text
        if answer in ['Разделы', 'Помощь/О боте', 'Обратная связь']:
            self.dp.handlers[1].clear()
            return

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
        with open('Json_data/' + str(self.chat_id) + '.json', mode='w') as file:
            json.dump(data, file)
            file.close()
        self.spisok_tasks.clear()

    def equations(self, update, _):
        equations_btns = self.global_slovar['Уравнения и неравенства']

        reply_markup = InlineKeyboardMarkup(equations_btns)
        self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                             text='Тема: ТРИГОНОМЕТРИЯ. Выберите подтемы:')

    def systems(self, update, _):
        systems_btns = self.global_slovar['Алгебраические системы']

        reply_markup = InlineKeyboardMarkup(systems_btns)
        self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                             text='Тема: ТРИГОНОМЕТРИЯ. Выберите подтемы:')

    def text_tasks(self, update, _):
        text_tasks_btns = self.global_slovar['Текстовые задачи']

        reply_markup = InlineKeyboardMarkup(text_tasks_btns)
        self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                             text='Тема: ТРИГОНОМЕТРИЯ. Выберите подтемы:')

    def parameters(self, update, _):
        parameters_btns = self.global_slovar['Параметры']

        reply_markup = InlineKeyboardMarkup(parameters_btns)
        self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                             text='Тема: ТРИГОНОМЕТРИЯ. Выберите подтемы:')

    def planimetry(self, update, _):
        planimetry_btns = self.global_slovar['Планиметрия']

        reply_markup = InlineKeyboardMarkup(planimetry_btns)
        self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                             text='Тема: ТРИГОНОМЕТРИЯ. Выберите подтемы:')

    def stereometry(self, update, _):
        stereometry_btns = self.global_slovar['Стереометрия']

        reply_markup = InlineKeyboardMarkup(stereometry_btns)
        self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                             text='Тема: ТРИГОНОМЕТРИЯ. Выберите подтемы:')

    def other_var(self, update, _):
        other_var_btns = self.global_slovar['Из вариантов олимпиад прошлых лет']

        reply_markup = InlineKeyboardMarkup(other_var_btns)
        self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                             text='Тема: ТРИГОНОМЕТРИЯ. Выберите подтемы:')

    def non_standart(self, update, _):
        non_standart_btns = self.global_slovar['Нестандартные задачи']

        reply_markup = InlineKeyboardMarkup(non_standart_btns)
        self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                             text='Тема: ТРИГОНОМЕТРИЯ. Выберите подтемы:')
