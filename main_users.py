# файл для тестовой записи в бд, давно не редактировался
from data import db_session
from data.users import BotUser


def main_ppppp():
    db_session.global_init("db/bot_db_tasks.db")
    session = db_session.create_session()

    user = BotUser()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    user.hashed_password = "cap"
    session.add(user)

    user = BotUser()
    user.surname = "Weir"
    user.name = "Andy"
    user.age = 18
    user.position = "chief scientist"
    user.speciality = "geologist"
    user.address = "module_1"
    user.email = "andy_chief@mars.org"
    user.hashed_password = "sci"
    session.add(user)

    user = BotUser()
    user.surname = "Watny"
    user.name = "Mark"
    user.age = 25
    user.position = "middle scientist"
    user.speciality = "biologist"
    user.address = "module_2"
    user.email = "mark@mars.org"
    user.hashed_password = "bio"
    session.add(user)

    user = BotUser()
    user.surname = "Kapoor"
    user.name = "Venkat"
    user.age = 15
    user.position = "pilot"
    user.speciality = "pilot, navigator"
    user.address = "module_2"
    user.email = "kapoor@mars.org"
    user.hashed_password = "pilot"
    session.add(user)

    user = BotUser()
    user.surname = "Sanders"
    user.name = "Teddy"
    user.age = 27
    user.position = "programmer"
    user.speciality = "IT specialist"
    user.address = "module_2"
    user.email = "sanders@mars.org"
    user.hashed_password = "comp"
    session.add(user)

    user = BotUser()
    user.surname = "Bean"
    user.name = "Sean"
    user.age = 17
    user.position = "chief engineer"
    user.speciality = "builder"
    user.address = "module_1"
    user.email = "bean@mars.org"
    user.hashed_password = "build"

    session.add(user)
    session.commit()


if __name__ == '__main__':
    main_ppppp()
