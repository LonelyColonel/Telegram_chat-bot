import logging
import telegram
import json
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from data import db_session
from data.users import BotUser

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.FileHandler('bot_logs.log', 'a', 'utf-8')
formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")
handler.setFormatter(formatter)
root_logger.addHandler(handler)


class MainBot:
    def __init__(self, token):
        self.token = token
        self.updater = Updater(self.token, use_context=True)
        self.dp = self.updater.dispatcher
        self.bot = telegram.Bot(self.token)
        self.reply_keyboard = [['Разделы'], ['Помощь/О боте', 'Статистика']]
        self.markup = ReplyKeyboardMarkup(self.reply_keyboard, one_time_keyboard=False)

    def start(self, update, context):
        self.chat_id = update.message.chat_id
        logging.info(f'Пользователь: id: {self.chat_id}, username: {update.message.chat.username}, '
                     f'first_name_user: {update.message.chat.first_name}, '
                     f'last_name_user: {update.message.chat.last_name}')
        chat_in_bot = update.message.chat
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        check_list = []
        for i in session.query(BotUser).filter(BotUser.chat_id_with_user == chat_in_bot.id):
            check_list.append(i)
        if len(check_list) != 1:
            user = BotUser()
            user.id_username = chat_in_bot.id
            user.username = chat_in_bot.username
            user.chat_id_with_user = chat_in_bot.id
            user.first_name_user = chat_in_bot.first_name
            user.last_name_user = chat_in_bot.last_name

            session.add(user)
            session.commit()

            with open('Json_data/template_json.json', mode='r') as file:
                slovar = json.load(file)
                file.close()
            with open(f'Json_data/{chat_in_bot.id}.json', mode='w') as file:
                json.dump(slovar, file)
                file.close()

        update.message.reply_text(
            'Бот запущен и готов к работе',
            reply_markup=self.markup
        )

    def help(self, update, context):
        update.message.reply_text(
            'Раздел "Помощь" \n1)Для выбора предметов нажмите на кнопку "Разделы"'
            '\n2)Также можно воспользоваться командами прописываемые в чат через "/"'
            '\n3)Доступные команды можно найти в меню(на мобильных версиях телеграмма)'
            '\n4)На десктопной(компьютерной) версии телеграмма можно написать "/" и появиться '
            'меню с командами'
            '\n5)Для ввода ответов(при проверке, после выполнения задания) нужно вводить строго по образцу,'
            'который будет представлен, если нажать на кнопку под этим сообщением'
            '\nКАК ВВОДИТЬ ОТВЕТЫ В ЧАТ-БОТ:'
            '\nРАЗДЕЛ МАТЕМАТИКА:'
            '\n1)sin(x), cos(x), tg(x), ctg(x), arcsin(x), arccos(x), arctg(x), arcctg(x)'
            '\n2)pi - число пи'
            '\n3)sqrt(x) - корень из числа'
            '\n4)* - произведение(писать обязательно, например не 2x, а 2*x)'
            '\n5)Дроби вводить только неправильные, целую часть не выделять'
            '\n6)При возможности все числа переводить в десятичную дробь'
            '\n7)При десятичной записи числа использовать запятую'
            '\nРАЗДЕЛ ФИЗИКА:'
            '\n1)Вводить число без указания единиц измерения'
            '\n2)Все числа в десятичной дроби'
            '\n3)При десятичной записи числа использовать запятую'
        )

    def about(self, update, context):
        btns = [[InlineKeyboardButton('Физика', callback_data='Phys_statistics'),
                 InlineKeyboardButton('Математика', callback_data='Maths_statistics')]]
        markup = InlineKeyboardMarkup(btns)
        update.message.reply_text(
            'Выберите, по какому предмету, вы хотите получить статистику?',
            reply_markup=markup
        )

    def statistic(self, update, context):
        query = update.callback_query
        variant = query.data
        query.answer()
        query.delete_message()
        chat_id = update.callback_query.message.chat.id
        with open(f'Json_data/{chat_id}.json', 'r') as file:
            slovar = json.load(file)
            file.close()
        spisok = []
        if variant == 'Maths_statistics':
            spisok.append(f"Правильно решённых задач: {len(slovar[1]['completed_maths'])}")
            spisok.append(f'Неправильно решённых задач: {len(slovar[1]["failed_maths"])}')
            self.bot.sendMessage(chat_id=chat_id, text=spisok[0] + '\n' + spisok[1])
        else:
            spisok.append(f"Правильно решённых задач: {len(slovar[0]['completed'])}")
            spisok.append(f'Неправильно решённых задач: {len(slovar[0]["failed"])}')
            self.bot.sendMessage(chat_id=chat_id, text=spisok[0] + '\n' + spisok[1])

    def sections(self, update, context):
        self.chat_id = update.message.chat_id
        button_list = [
            [InlineKeyboardButton("Физика(ЕГЭ)", callback_data='1')],
            [InlineKeyboardButton("Математика(олимпиады)", callback_data='2')],
        ]
        reply_markup = InlineKeyboardMarkup(button_list)
        update.message.reply_text(text="Разделы:", reply_markup=reply_markup)

    def choice(self, update, _):
        query = update.callback_query
        variant = query.data
        query.answer()
        query.delete_message()
        if variant == '1':
            from physics_class import Physics
            self.work_class = Physics(self.token, self.bot, self.chat_id, self.dp)
            self.work_class.main_physics()

        elif variant == '2':
            from maths_class import Maths
            self.work_class = Maths(self.token, self.bot, self.chat_id, self.dp)
            self.work_class.main_maths()

    def admin_func(self, update, _):
        with open(file='admin_list_file.txt', encoding='utf-8', mode='r') as admin_list_file:
            admin_list = admin_list_file.read().split('\n')
            admin_list_file.close()
        if update.message.chat.username in admin_list:
            from admin_class import Admin
            logging.info(f'Пользователь: id: {self.chat_id}, username: {update.message.chat.username}, '
                         f'first_name_user: {update.message.chat.first_name}, '
                         f'last_name_user: {update.message.chat.last_name}'
                         f'Вошёл в режим администратора')
            update.message.reply_text('Приветствую хозяин, теперь ты дома.')
            self.work_class = Admin(self.token, self.bot, update.message.chat.id, self.dp)
            self.work_class.admin_main()

    def main(self):
        self.dp.add_handler(MessageHandler(Filters.regex('Помощь/О боте'), self.help))
        self.dp.add_handler(CommandHandler('start', self.start))
        self.dp.add_handler(CommandHandler('help', self.help))
        self.dp.add_handler(CommandHandler('sections', self.sections))
        self.dp.add_handler(CommandHandler('admin', self.admin_func))
        self.dp.add_handler(MessageHandler(Filters.regex('Статистика'), self.about))
        self.dp.add_handler(MessageHandler(Filters.regex('Разделы'), self.sections))
        self.dp.add_handler(CallbackQueryHandler(self.choice, pattern='1'))
        self.dp.add_handler(CallbackQueryHandler(self.choice, pattern='2'))
        self.dp.add_handler(CallbackQueryHandler(self.statistic, pattern='Phys_statistics'))
        self.dp.add_handler(CallbackQueryHandler(self.statistic, pattern='Maths_statistics'))

        self.updater.start_polling()
        self.updater.idle()


if __name__ == '__main__':
    main_bot = MainBot('5136885850:AAFx-0jdcaXWeiY-0VObbXdFaECnQiku2nc')
    db_session.global_init("db/bot_db.db")
    main_bot.main()
