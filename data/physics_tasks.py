import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class PhysicsTasks(SqlAlchemyBase):
    __tablename__ = 'physics_tasks'

    id_physics_tasks = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    theme_physics = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    number_physics = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    difficulty_physics = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    way_physics = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    answer_physics = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    solution_physics = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<PhysicsTasks> {self.id_physics_tasks} {self.theme_physics} {self.number_physics} ' \
               f'{self.difficulty_physics} {self.way_physics} {self.answer_physics} {self.solution_physics} ' \
               f'{self.created_date}'
