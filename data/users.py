import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class BotUser(SqlAlchemyBase):
    __tablename__ = 'users'

    number = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_username = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, index=True)
    username = sqlalchemy.Column(sqlalchemy.String)
    chat_id_with_user = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    first_name_user = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    last_name_user = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    def __repr__(self):
        return f'<BotUser>-{self.id_username}'

