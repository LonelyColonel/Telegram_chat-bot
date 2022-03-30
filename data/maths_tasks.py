import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class MathsTasks(SqlAlchemyBase):
    __tablename__ = 'maths_tasks'

    id_maths_tasks = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    # number_tasks_maths = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, index=True)
    theme_maths = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    undertheme_maths = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    difficulty_maths = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    way_maths = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    answer_maths = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    solution_maths = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    def __repr__(self):
        return f'<MathsTasks> {self.id_maths_tasks} {self.theme_maths} {self.undertheme_maths} ' \
               f'{self.difficulty_maths} {self.way_maths} {self.answer_maths} {self.solution_maths} ' \
               f'{self.created_date}'
