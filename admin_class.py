import logging
import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, ChosenInlineResultHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, User
from data import db_session
from main_class import MainBot
from PIL import Image
from data.maths_tasks import MathsTasks
from data.physics_tasks import PhysicsTasks


global_spisok_names = ['Тригонометрия', 'Уравнения и неравенства', 'Алгебраические системы', 'Текстовые задачи',
                       'Параметры', 'Планиметрия', 'Стереометрия', 'Из вариантов олимпиад прошлых лет',
                       'Нестандартные задачи']


class Admin(MainBot):
    def __init__(self, token, bot, chat_id, dp):
        super().__init__(token)
        self.bot = bot
        self.chat_id = chat_id
        self.dp = dp
        self.dictionary_maths = {
                                 'theme_maths': '',
                                 'undertheme_maths': '',
                                 'difficulty_maths': '',
                                 'way_maths': '',
                                 'answer_maths': '',
                                 'solution_maths': ''
                                 }
        self.dictionary_physics = {
                                   'theme_physics': '',
                                   'number_physics': '',
                                   'difficulty_physics': '',
                                   'way_physics': '',
                                   'answer_physics': '',
                                   'solution_physics': ''
                                  }

    def create_new_task(self, update, _):
        self.dp.add_handler(CallbackQueryHandler(self.create_tasks, pattern='PHY_ADM'))
        self.dp.add_handler(CallbackQueryHandler(self.create_tasks, pattern='MATHS_ADM'))
        button_list = [
            [InlineKeyboardButton("Физика", callback_data='PHY_ADM')],
            [InlineKeyboardButton("Математика", callback_data='MATHS_ADM')]]
        reply_markup = InlineKeyboardMarkup(button_list)
        self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                             text='Для какого предмета новое задание?')

    def create_tasks(self, update, _):
        query = update.callback_query
        variant = query.data
        query.answer()
        if variant == 'MATHS_ADM':
            self.subj = 'M'
            self.bot.sendMessage(chat_id=self.chat_id, text='Выбрана: Математика. Теперь пришли мне '
                                                            'тему в которую мне записать задание.'
                                                            '(вводить: превая буква большая, остальные маленькие) \n'
                                                            'Все темы: \n'
                                                            '1)TRIGONOMETRY(Тригонометрия) \n'
                                                            '2)EQUATIONS(Уравнения и неравенства) \n'
                                                            '3)SYSTEM(Алгебраические системы) \n'
                                                            '4)TEXT_TASKS(Текстовые задачи) \n'
                                                            '5)PARAMETERS(Параметры) \n'
                                                            '6)PLANIMETRY(Планиметрия) \n'
                                                            '7)STEREOMETRY(Стереометрия) \n'
                                                            '8)OTHER_VAR(Из вариантов олимпиад прошлых лет) \n'
                                                            '9)NON_STANDART(Нестандартные задачи)')
            self.dp.add_handler(MessageHandler(Filters.regex('^(TRIGONOMETRY|EQUATIONS|SYSTEM|TEXT_TASKS|PARAMETERS|'
                                                             'PLANIMETRY|STEREOMETRY|OTHER_VAR|NON_STANDART)$'),
                                               self.get_under_theme))
        elif variant == 'PHY_ADM':
            self.subj = 'P'
            self.bot.sendMessage(chat_id=self.chat_id, text='Выбрана: Физика. Теперь пришли мне '
                                                            'тему в которую мне записать задание.'
                                                            '(вводить: превая буква большая, остальные маленькие) \n'
                                                            'Все темы: \n'
                                                            '1)Механика\n'
                                                            '2)МКТ и термодинамика\n'
                                                            '3)Электродинамика\n'
                                                            '4)Оптика\n'
                                                            '5)Квантовая физика\n')
            self.dp.add_handler(MessageHandler(Filters.text('Механика' or 'МКТ и термодинамика' or
                                                            'Электродинамика' or 'Оптика'
                                                            or 'Квантовая физика'), self.get_under_theme))

    def get_under_theme(self, update, _):
        if self.subj == 'M':
            self.theme_maths = update.message.text
            self.dictionary_maths['theme_maths'] = self.theme_maths
            self.bot.sendMessage(chat_id=self.chat_id, text=f'Выбрано: {self.theme_maths}. Теперь выберите подтему.\n'
                                                            f'Подтемы:\n'
                                                            f'Тригонометрия:\n'
                                                            f'1)TRIGONOMETRY_EQUATIONS(Триг. ур-ия)\n'
                                                            f'2)Сведение к кв-ым триг. ур-ям\n'
                                                            f'3)Однородные ур-ия\n'
                                                            f'4)Системы триг. уравнений\n'
                                                            f'5)Преобразование триг. уравнений\n'
                                                            f'6)Обратные триг. функции\n'
                                                            f'7)Метод вспомогательного угла в триг.\n')
            self.dp.add_handler(MessageHandler(Filters.text('^(TRIGONOMETRY_EQUATIONS|Сведение к кв-ым триг. ур-ям|'
                                                            'Однородные ур-ия|Системы триг. уравнений|'
                                                            'Преобразование триг. уравнений|Обратные триг. функции|'
                                                            'Метод вспомогательного угла в триг.)$'),
                                               self.get_difficulty))
        elif self.subj == 'P':
            self.theme_physics = update.message.text
            self.dictionary_physics['theme_physics'] = self.theme_physics
            self.bot.sendMessage(chat_id=self.chat_id, text=f'Выбрано: {self.theme_physics}. Теперь выберите номер.\n'
                                                            f'число от 1-30 + _ + слово "номер". Например: 1_номер')

            self.dp.add_handler(MessageHandler(Filters.text('1_номер' or '2_номер' or '3_номер' or '4_номер'
                                                            or '5_номер' or '6_номер' or '7_номер' or '8_номер' or
                                                            '9_номер' or '10_номер' or '11_номер' or '12_номер' or
                                                            '13_номер' or '14_номер' or '15_номер' or
                                                            '16_номер' or '17_номер' or '18_номер' or '19_номер' or
                                                            '20_номер' or '21_номер' or '22_номер' or '23_номер' or
                                                            '24_номер' or '25_номер' or
                                                            '26_номер' or '27_номер' or '28_номер' or '29_номер' or
                                                            '30_номер'), self.get_difficulty))

    def get_difficulty(self, update, _):
        undertheme = update.message.text
        self.dictionary_maths['undertheme_maths'] = undertheme
        self.dictionary_physics['number_physics'] = undertheme

        self.bot.sendMessage(chat_id=self.chat_id, text=f'Теперь скажи, какая сложность у этого задания: '
                                                        f'Л - лёгкая, С - средняя, Т - тяжёлая')
        self.dp.add_handler(MessageHandler(Filters.regex('Л|С|Т'), self.get_task_photo))

    def get_task_photo(self, update, _):
        self.difficulty = update.message.text
        self.dictionary_maths['difficulty_maths'] = self.difficulty
        self.dictionary_physics['difficulty_physics'] = self.difficulty
        self.bot.sendMessage(chat_id=self.chat_id, text='Теперь пришли мне '
                                                        'условие(фото)')
        self.dp.add_handler(MessageHandler(Filters.document, self.get_photo_handler_func), group=1)

    def png_to_jpeg(self, way):
        photo = Image.open(way)
        photo = photo.convert('RGB')
        new_way = way.split('.')[0]
        photo.save(new_way + '.jpeg', format='jpeg', quality=50)

    def get_photo_handler_func(self, update, context):
        # print(update.message)
        file = update.message.document.file_id
        filename = update.message.document.file_name
        # print(filename)
        obj = context.bot.get_file(file)
        obj.download('tasks/' + filename)

        if filename.split('.')[1] == 'png':
            self.png_to_jpeg('tasks/' + filename)
            filename = filename.split('.')[0] + '.jpeg'

        self.dictionary_maths['way_maths'] = 'tasks/' + filename
        self.dictionary_physics['way_physics'] = 'tasks/' + filename
        self.bot.sendMessage(chat_id=self.chat_id, text='Теперь пришли мне '
                                                        'ответ на это задание')
        # print(self.dp.handlers)
        self.dp.handlers[1].clear()
        self.dp.add_handler(MessageHandler(Filters.text, self.get_answer_func), group=1)

    def get_answer_func(self, update, context):
        self.answer = update.message.text
        self.dp.handlers[1].clear()
        self.dictionary_maths['answer_maths'] = self.answer
        self.dictionary_physics['answer_physics'] = self.answer
        self.bot.sendMessage(chat_id=self.chat_id, text='Теперь пришли мне '
                                                        'решение этого задания(фото)')
        self.dp.add_handler(MessageHandler(Filters.document, self.get_solution_func), group=1)

    def get_solution_func(self, update, context):
        file = update.message.document.file_id
        filename = update.message.document.file_name
        obj = context.bot.get_file(file)
        obj.download('solutions/' + filename)

        if filename.split('.')[1] == 'png':
            self.png_to_jpeg('solutions/' + filename)
            filename = filename.split('.')[0] + '.jpeg'

        self.dictionary_maths['solution_maths'] = 'solutions/' + filename
        self.dictionary_physics['solution_physics'] = 'solutions/' + filename
        self.dp.handlers[1].clear()
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        if self.subj == 'M':
            task_math = MathsTasks()
            task_math.theme_maths = self.dictionary_maths['theme_maths']
            task_math.undertheme_maths = self.dictionary_maths['undertheme_maths']
            task_math.difficulty_maths = self.dictionary_maths['difficulty_maths']
            task_math.way_maths = self.dictionary_maths['way_maths']
            task_math.answer_maths = self.dictionary_maths['answer_maths']
            task_math.solution_maths = self.dictionary_maths['solution_maths']
            task_math.win_or_fail_or_unresolved = 'N'

            session.add(task_math)
            session.commit()
        elif self.subj == 'P':
            task_physics = PhysicsTasks()
            task_physics.theme_physics = self.dictionary_physics['theme_physics']
            task_physics.number_physics = self.dictionary_physics['number_physics']
            task_physics.difficulty_physics = self.dictionary_physics['difficulty_physics']
            task_physics.way_physics = self.dictionary_physics['way_physics']
            task_physics.answer_physics = self.dictionary_physics['answer_physics']
            task_physics.solution_physics = self.dictionary_physics['solution_physics']

            session.add(task_physics)
            session.commit()
        self.bot.sendMessage(chat_id=self.chat_id, text='Успешно добавлено в базу данных!')

        # print(self.dictionary_maths)
        # print(self.dictionary_physics)

    def for_see_lastest_addition_maths(self, update, _):
        try:
            db_session.global_init("db/bot_db.db")
            session = db_session.create_session()
            text_temp = session.query(MathsTasks).all()[-1]
            print(type(text_temp))
            print(session.query(MathsTasks).all()[-1])
            self.bot.sendMessage(chat_id=self.chat_id, text=str(text_temp))
        except IndexError:
            self.bot.sendMessage(chat_id=self.chat_id, text='В базе данных нет ни одного задания по математике')

    def for_see_lastest_addition_physics(self, update, _):
        try:
            db_session.global_init("db/bot_db.db")
            session = db_session.create_session()
            text_temp = session.query(PhysicsTasks).all()[-1]
            print(type(text_temp))
            print(session.query(PhysicsTasks).all()[-1])
            self.bot.sendMessage(chat_id=self.chat_id, text=str(text_temp))
        except IndexError:
            self.bot.sendMessage(chat_id=self.chat_id, text='В базе данных нет ни одного задания по физике')

    def admin_main(self):
        self.dp.add_handler(CommandHandler('new_task', self.create_new_task))
        self.dp.add_handler(CommandHandler('see_the_latest_addition_maths', self.for_see_lastest_addition_maths))
        self.dp.add_handler(CommandHandler('see_the_latest_addition_physics', self.for_see_lastest_addition_physics))

        text_for_admin = 'Команды для управления ботом от имени администратора:\n' \
                         '/new_task - для создания нового задания и добавления его в базу данных\n' \
                         '/see_the_latest_addition_maths - для просмотра последней добавленной задачи в раздел ' \
                         'математика\n' \
                         '/see_the_latest_addition_physics - для просмотра последней добавленной задачи в раздел ' \
                         'физика'
        self.bot.sendMessage(chat_id=self.chat_id, text=text_for_admin)
