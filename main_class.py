import logging
import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, ChosenInlineResultHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, User
from data import db_session
from main_users import main_ppppp
from data.users import BotUser
# from physics_class import Physics
# from maths_class import Maths
# import physics_class
# import maths_class

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class MainBot:
    def __init__(self, token):
        self.token = token
        self.updater = Updater(self.token, use_context=True)
        self.dp = self.updater.dispatcher
        self.bot = telegram.Bot(self.token)
        # self.chat_id = self.bot.get_updates()[-1].message.chat_id
        self.reply_keyboard = [['Разделы'], ['Помощь/О боте', 'Обратная связь']]
        self.markup = ReplyKeyboardMarkup(self.reply_keyboard, one_time_keyboard=False)

    def start(self, update, context):
        # print(self.bot.get_updates())
        # main_ppppp()
        print(update.message)
        print('--------------------------------------------------------------------------')
        # print(update.message.from.id)
        chat_in_bot = update.message.chat
        db_session.global_init("db/bot_db.db")
        session = db_session.create_session()
        check_list = []
        for i in session.query(BotUser).filter(BotUser.chat_id_with_user == chat_in_bot.id):
            check_list.append(i)
        print(check_list)
        if len(check_list) != 1:
            user = BotUser()
            user.id_username = chat_in_bot.id
            user.username = chat_in_bot.username
            user.chat_id_with_user = chat_in_bot.id
            user.first_name_user = chat_in_bot.first_name
            user.last_name_user = chat_in_bot.last_name

            # user.unresolved_maths =

            session.add(user)
            session.commit()
        # print(update)
        update.message.reply_text(
            'Бот запущен и готов к работе',
            reply_markup=self.markup
        )

    def help(self, update, context):
        update.message.reply_text(
            'Раздел "Помощь" \n1)Для выбора предметов нажмите на кнопку "Разделы"'
            '\n2)Также можно воспользоваться командами прописываемые в чат через "/"'
            '\n3)Доступные команды можно найти в меню(на мобильных версиях телеграмма)'
            '\n4)На десктопной(компьютерной) версии телеграмма можно написать "/" и появиться'
            'меню с командами'
            '\n5)Для ввода ответов(при проверке, после выполнения задания) нужно вводить строго по образцу,'
            'который будет представлен, если нажать на кнопку под этим сообщением'
        )

    def about(self, update, context):
        update.message.reply_text(
            'Не знаю какой здесь будет текст, это тестовая запись',
            reply_markup=self.markup
        )

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
            print(admin_list)
            admin_list_file.close()
        if update.message.chat.username in admin_list:
            from admin_class import Admin
            self.work_class = Admin(self.token, self.bot, update.message.chat.id, self.dp)
            self.work_class.admin_main()
            update.message.reply_text('Приветствую хозяин, теперь ты дома.')

    def main(self):
        self.dp.add_handler(MessageHandler(Filters.regex('Помощь/О боте'), self.help))
        self.dp.add_handler(CommandHandler('start', self.start))
        self.dp.add_handler(CommandHandler('help', self.help))
        self.dp.add_handler(CommandHandler('sections', self.sections))
        self.dp.add_handler(CommandHandler('admin', self.admin_func))
        self.dp.add_handler(MessageHandler(Filters.regex('Обратная связь'), self.about))
        self.dp.add_handler(MessageHandler(Filters.regex('Разделы'), self.sections))
        self.dp.add_handler(CallbackQueryHandler(self.choice, pattern='1'))
        self.dp.add_handler(CallbackQueryHandler(self.choice, pattern='2'))
        self.updater.start_polling()
        self.updater.idle()


if __name__ == '__main__':
    main_bot = MainBot('5136885850:AAFx-0jdcaXWeiY-0VObbXdFaECnQiku2nc')
    db_session.global_init("db/bot_db.db")
    main_bot.main()
