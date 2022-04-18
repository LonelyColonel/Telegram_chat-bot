# импорт необходимых модулей
import logging
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from data import db_session
from main_class import MainBot
from PIL import Image
from data.maths_tasks import MathsTasks
from data.physics_tasks import PhysicsTasks
from data.users import BotUser


global_spisok_names = ['Тригонометрия', 'Уравнения и неравенства', 'Алгебраические системы', 'Текстовые задачи',
                       'Параметры', 'Планиметрия', 'Стереометрия', 'Из вариантов олимпиад прошлых лет',
                       'Нестандартные задачи']


# Admin - класс для удобного добавления новых задач, для этого администратору нужно
# написать чат-боту команду "/admin" и следовать указаниям, наследуется от MainBot
class Admin(MainBot):
    def __init__(self, token, chat_id, dp, bot):
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

    # функция для создания новых заданий
    def create_new_task(self, update, _):
        self.chat_id = update.message.chat_id
        self.dp.add_handler(CallbackQueryHandler(self.create_tasks, pattern='PHY_ADM'))
        self.dp.add_handler(CallbackQueryHandler(self.create_tasks, pattern='MATHS_ADM'))
        # создание кнопок под сообщением
        button_list = [
            [InlineKeyboardButton("Физика", callback_data='PHY_ADM')],
            [InlineKeyboardButton("Математика", callback_data='MATHS_ADM')]]
        reply_markup = InlineKeyboardMarkup(button_list)
        # бот отправляет сообщение с кнопками под ним
        self.bot.sendMessage(chat_id=self.chat_id, reply_markup=reply_markup,
                             text='Для какого предмета новое задание?')

    # функция для получения предмета от админа
    def create_tasks(self, update, _):
        self.chat_id = update.callback_query.message.chat.id
        # получаем callback от нажатой кнопки
        query = update.callback_query
        variant = query.data
        query.answer()
        # сверяемся
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
            # регистрируем обработчики
            self.dp.add_handler(MessageHandler(Filters.regex('^(TRIGONOMETRY|EQUATIONS|SYSTEM|TEXT_TASKS|PARAMETERS|'
                                                             'PLANIMETRY|STEREOMETRY|OTHER_VAR|NON_STANDART)$'),
                                               self.get_under_theme))
        elif variant == 'PHY_ADM':
            self.subj = 'P'
            self.bot.sendMessage(chat_id=self.chat_id, text='Выбрана: Физика. Теперь пришли мне '
                                                            'тему в которую мне записать задание.'
                                                            '(вводить: превая буква большая, остальные маленькие) \n'
                                                            'Все темы: \n'
                                                            '1)Mechanics\n'
                                                            '2)MKT and thermodynamics\n'
                                                            '3)Electrodynamics\n'
                                                            '4)Optics\n'
                                                            '5)Quantum physics\n')
            text = '^(Mechanics|MKT and thermodynamics|Electrodynamics|Optics|Quantum physics)$'
            # регистрируем обработчики
            self.dp.add_handler(MessageHandler(Filters.text(text), self.get_under_theme))

    # функция для получения от админа подтемы или номера (в зависимости от предмета)
    def get_under_theme(self, update, _):
        self.chat_id = update.message.chat_id
        if self.subj == 'M':
            self.theme_maths = update.message.text
            self.dictionary_maths['theme_maths'] = self.theme_maths
            self.bot.sendMessage(chat_id=self.chat_id, text=f'Выбрано: {self.theme_maths}. Теперь выберите подтему.\n'
                                                            f'Подтемы:\n'
                                                            f'Тригонометрия:\n'
                                                            f'1)TRIGONOMETRY_EQUATIONS (Триг. ур-ия)\n'
                                                            f'2)SQUARE_EQUATIONS (Сведение к кв-ым триг. ур-ям)\n'
                                                            f'3)SINGLE_TRIGONOMETRY (Однородные ур-ия)\n'
                                                            f'4)TRIGONOMETRY_SYSTEM (Системы триг. уравнений)\n'
                                                            f'5)TRANSFORMATIONS (Преобразование триг. уравнений)\n'
                                                            f'6)INVERSE_FUNCTIONS (Обратные триг. функции)\n'
                                                            f'7)SUPPORT_ANGLE (Метод вспомогательного угла в триг.)\n'
                                                            f'Уравнения и неравенства:\n'
                                                            f'1)MODULO_EQUATIONS(Уравнения и неравенства с модулем)\n'
                                                            f'2)RATIONAL_EQUATIONS(Рациональные уравнения и '
                                                            f'неравенства)\n'
                                                            f'3)EQUATIONS_WITH_RADICALS(Уравнения и неравенства с '
                                                            f'радикалами)\n'
                                                            f'4)EXPONENTIAL_EQUATIONS(Показательные уравнения)\n'
                                                            f'5)LOGARITHMIC_EQUATIONS(Логарифмические уравнения)\n'
                                                            f'6)MIXED_TRIGONOMETRY(Смешанная тригонометрия)\n'
                                                            f'7)MIXED_EQUATIONS(Смешанные уравнения)\n'
                                                            f'Алгебраические системы:\n'
                                                            f'1)SIMPLE_EQUATION_SYSTEMS(Простые системы уравнений)\n'
                                                            f'2)SQUARE_EQUATIONS(Сложные системы уравнений)\n'
                                                            f'3)ARISING_FROM_TEXT_TASKS(Возникающие из текстовых '
                                                            f'задач)\n'
                                                            f'Текстовые задачи:\n'
                                                            f'1)MOVEMENT_TASKS(Задачи на движение)\n'
                                                            f'2)TASKS_FOR_WORK(Задачи на работу)\n'
                                                            f'3)TASKS_ON_MIXTURES(Задачи на смеси)\n'
                                                            f'4)PROGRESSION_TASKS(Задачи на прогрессии)\n'
                                                            f'5)OPTIMAL_CHOICE(Оптимальный выбор и целые числа)\n'
                                                            f'Параметры:\n'
                                                            f'1)SQUARE_EQ_NERVES_PARAMETER(Квадратные ур-ия и нер-ва с '
                                                            f'параметром)\n'
                                                            f'2)LOGICAL_TASKS(Логические задачи)\n'
                                                            f'3)DIFFICULT_LOG_TASKS(Сложные логические задачи)\n'
                                                            f'4)WITH_ROOTS(Параметры с корнями)\n'
                                                            f'Планиметрия:\n'
                                                            f'1)COMMON_TRIANGLES(Общие треугольники)\n'
                                                            f'2)SEMBLANCE(Подобие)\n'
                                                            f'3)SQUARES(Площади)\n'
                                                            f'4)PARALLEL_TRAPEZOIDS(Параллелограммы и трапеции)\n'
                                                            f'5)CIRCLES(Окружности)\n'
                                                            f'6)BUILDINGS(Построения)\n'
                                                            f'Стереометрия:\n'
                                                            f'1)()\n'
                                                            f'2)()\n'
                                                            f'3)()\n'
                                                            f'4)()\n'
                                                            f'5)()\n'
                                                            f'6)()\n'
                                                            f'Из вариантов олимпиад прошлых лет:\n'
                                                            f'1)PHYSTECH(Физтех)\n'
                                                            f'2)OMMO(ОММО)\n'
                                                            f'3)PVG(ПВГ)\n'
                                                            f'4)LOMONOSOV(Ломоносов)\n'
                                                            f'5)ROSATOM(Росатом)\n'
                                                            f'6)SAMMAT(САММАТ)\n'
                                                            f'7)GAZPROM(Газпром)\n'
                                                            f'Нестандартные задачи:\n'
                                                            f'1)MAJOR_METHOD(Метод мажорант)\n'
                                                            f'2)FUNCTIONS(Использование св-в функций)\n'
                                                            f'3)GROUPING(Подстановка или группировка)\n'
                                                            f'4)GEOMETRIC_APPROACH(Геометрический подход)')
            self.dp.add_handler(MessageHandler(Filters.text('^(TRIGONOMETRY_EQUATIONS|SQUARE_EQUATIONS|'
                                                            'SINGLE_TRIGONOMETRY|TRIGONOMETRY_SYSTEM|'
                                                            'TRANSFORMATIONS|INVERSE_FUNCTIONS|'
                                                            'SUPPORT_ANGLE|MODULO_EQUATIONS|RATIONAL_EQUATIONS|'
                                                            'EQUATIONS_WITH_RADICALS|EXPONENTIAL_EQUATIONS|'
                                                            'LOGARITHMIC_EQUATIONS|MIXED_TRIGONOMETRY|'
                                                            'MIXED_EQUATIONS|SIMPLE_EQUATION_SYSTEMS|SQUARE_EQUATIONS|'
                                                            'ARISING_FROM_TEXT_TASKS|MOVEMENT_TASKS|'
                                                            'TASKS_FOR_WORK|TASKS_ON_MIXTURES|'
                                                            'PROGRESSION_TASKS|OPTIMAL_CHOICE|'
                                                            'SQUARE_EQ_NERVES_PARAMETER|'
                                                            'LOGICAL_TASKS|DIFFICULT_LOG_TASKS|'
                                                            'WITH_ROOTS|COMMON_TRIANGLES|'
                                                            'SEMBLANCE|SQUARES|PARALLEL_TRAPEZOIDS|'
                                                            'CIRCLES|BUILDINGS|'
                                                            'PHYSTECH|OMMO|'
                                                            'PVG|LOMONOSOV|ROSATOM|'
                                                            'SAMMAT|GAZPROM|'
                                                            'MAJOR_METHOD|FUNCTIONS|'
                                                            'GROUPING|GEOMETRIC_APPROACH)$'),
                                               self.get_difficulty))
        elif self.subj == 'P':
            self.theme_physics = update.message.text
            self.dictionary_physics['theme_physics'] = self.theme_physics
            self.bot.sendMessage(chat_id=self.chat_id, text=f'Выбрано: {self.theme_physics}. Теперь выберите номер.\n'
                                                            f'число от 1-30')
            text = '^(1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30)$'
            self.dp.add_handler(MessageHandler(Filters.text(text), self.get_difficulty))

    # функция для получения сложности от админа
    def get_difficulty(self, update, _):
        self.chat_id = update.message.chat_id
        # получаем текст, который написал в ответ админ
        undertheme = update.message.text
        self.dictionary_maths['undertheme_maths'] = undertheme
        self.dictionary_physics['number_physics'] = undertheme

        self.bot.sendMessage(chat_id=self.chat_id, text=f'Теперь скажи, какая сложность у этого задания: '
                                                        f'Л - лёгкая, С - средняя, Т - тяжёлая')
        self.dp.add_handler(MessageHandler(Filters.regex('Л|С|Т'), self.get_task_photo))

    # для анализа ответа админа из предыдущей функции
    def get_task_photo(self, update, _):
        self.chat_id = update.message.chat_id
        self.difficulty = update.message.text
        self.dictionary_maths['difficulty_maths'] = self.difficulty
        self.dictionary_physics['difficulty_physics'] = self.difficulty
        self.bot.sendMessage(chat_id=self.chat_id, text='Теперь пришли мне '
                                                        'условие(фото)')
        self.dp.add_handler(MessageHandler(Filters.document, self.get_photo_handler_func), group=1)

    # для преобразования картинки из png в jpeg
    def png_to_jpeg(self, way):
        photo = Image.open(way)
        photo = photo.convert('RGB')
        new_way = way.split('.')[0]
        photo.save(new_way + '.jpeg', format='jpeg', quality=50)

    # для получения фото в виде документа.
    def get_photo_handler_func(self, update, context):
        self.chat_id = update.message.chat_id
        file = update.message.document.file_id
        filename = update.message.document.file_name
        obj = context.bot.get_file(file)
        obj.download('tasks/' + filename)
        # проверяем если загруженный админом документ(картинка) в формате png то преобразуем в jpeg
        if filename.split('.')[1] == 'png':
            self.png_to_jpeg('tasks/' + filename)
            filename = filename.split('.')[0] + '.jpeg'

        # добавляем всё в словарь, данные из которого, после записи всех данных отправляются в базу данных
        self.dictionary_maths['way_maths'] = 'tasks/' + filename
        self.dictionary_physics['way_physics'] = 'tasks/' + filename
        self.bot.sendMessage(chat_id=self.chat_id, text='Теперь пришли мне '
                                                        'ответ на это задание')
        # очищаем список обработчиков (при регистрации обработчика можно указать либо 1-ую группу, либо
        # ничего, тогда этот обработчик по умолчанию добавляется в 0 группу, а так как в функции get_task_photo
        # обработчик мы зарегистрировали в 1 группу, то оттуда его нужно очистить, чтобы не возникала путанница)
        self.dp.handlers[1].clear()
        # объявляем новый обработчик
        self.dp.add_handler(MessageHandler(Filters.text, self.get_answer_func), group=1)

    # анализ ответа и отправка сообщения с просьбой отправить фото с заданием
    def get_answer_func(self, update, context):
        self.chat_id = update.message.chat_id
        self.answer = update.message.text
        self.dp.handlers[1].clear()
        self.dictionary_maths['answer_maths'] = self.answer
        self.dictionary_physics['answer_physics'] = self.answer
        self.bot.sendMessage(chat_id=self.chat_id, text='Теперь пришли мне '
                                                        'решение этого задания(фото)')
        # объявляем новый обработчик
        self.dp.add_handler(MessageHandler(Filters.document, self.get_solution_func), group=1)

    # функция для записи всех собранных данных в бд
    def get_solution_func(self, update, context):
        self.chat_id = update.message.chat_id
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

        # открываем соединение с базой данных
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

    # для просмотра названия, id и так далее, последней добавленной задачи
    def for_see_lastest_addition_maths(self, update, _):
        self.chat_id = update.message.chat_id
        try:
            db_session.global_init("db/bot_db.db")
            session = db_session.create_session()
            text_temp = session.query(MathsTasks).all()[-1]
            self.bot.sendMessage(chat_id=self.chat_id, text=str(text_temp))
        except IndexError:
            self.bot.sendMessage(chat_id=self.chat_id, text='В базе данных нет ни одного задания по математике')

    # тоже самое что и в предыдущей функции, но только для физики
    def for_see_lastest_addition_physics(self, update, _):
        self.chat_id = update.message.chat_id
        try:
            db_session.global_init("db/bot_db.db")
            session = db_session.create_session()
            text_temp = session.query(PhysicsTasks).all()[-1]
            self.bot.sendMessage(chat_id=self.chat_id, text=str(text_temp))
        except IndexError:
            self.bot.sendMessage(chat_id=self.chat_id, text='В базе данных нет ни одного задания по физике')

    # функции для отправки сообщения админом через бот, какому-нибудь другом пользователю
    def send_message_user_func(self, update, _):
        self.chat_id = update.message.chat_id
        self.bot.sendMessage(chat_id=self.chat_id, text='Введите id пользователя, которому хотите отправить сообщение')
        update.message.text = ''
        self.dp.add_handler(MessageHandler(Filters.text, self.send_mes_func_text), group=1)

    def send_mes_func_text(self, update, _):
        self.u_id = update.message.text
        if self.u_id:
            self.dp.handlers[1].clear()
            self.bot.sendMessage(chat_id=update.message.chat_id, text='Теперь отправьте текст')
            self.dp.add_handler(MessageHandler(Filters.text, self.send_mes_func), group=1)

    def send_mes_func(self, update, _):
        self.text = update.message.text
        self.dp.handlers[1].clear()
        self.bot.sendMessage(chat_id=self.u_id, text=self.text)
        self.bot.sendMessage(chat_id=update.message.chat_id, text='Успешно отправлено пользователю!')

    def send_message_users_func_text(self, update, _):
        self.bot.sendMessage(chat_id=update.message.chat_id, text='Отправьте текст')
        update.message.text = ''
        self.dp.add_handler(MessageHandler(Filters.text, self.send_message_users_func), group=1)

    def send_message_users_func(self, update, _):
        spisok = []
        self.text_asnwer = update.message.text
        if self.text_asnwer:
            self.dp.handlers[1].clear()
            db_session.global_init("db/bot_db.db")
            session = db_session.create_session()
            # добавление всех id из бд в список
            for i in session.query(BotUser).filter(BotUser.id_username):
                spisok.append(i)
            # отправка всем пользователям бота сообщения, которое отправил админ боту
            for i in spisok:
                self.bot.sendMessage(chat_id=int(str(i)), text=self.text_asnwer)
            self.bot.sendMessage(chat_id=update.message.chat_id, text='Успешно отправлено пользователям!')

    # главная функция для данного класса
    def admin_main(self):
        # регистрация обработчиков
        self.dp.add_handler(CommandHandler('new_task', self.create_new_task))
        self.dp.add_handler(CommandHandler('see_the_latest_addition_maths', self.for_see_lastest_addition_maths))
        self.dp.add_handler(CommandHandler('see_the_latest_addition_physics', self.for_see_lastest_addition_physics))
        self.dp.add_handler(CommandHandler('send_message_user', self.send_message_user_func))
        self.dp.add_handler(CommandHandler('send_message_users', self.send_message_users_func_text))

        text_for_admin = 'Команды для управления ботом от имени администратора:\n' \
                         '/new_task - для создания нового задания и добавления его в базу данных\n' \
                         '/see_the_latest_addition_maths - для просмотра последней добавленной задачи в раздел ' \
                         'математика\n' \
                         '/see_the_latest_addition_physics - для просмотра последней добавленной задачи в раздел ' \
                         'физика\n' \
                         '/send_message_user - для отправки сообщения ОДНОМУ конкретному пользователю\n' \
                         '/send_message_users - для отправки сообщения ВСЕМ пользователям'
        self.bot.sendMessage(chat_id=self.chat_id, text=text_for_admin)
