from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from sqlalchemy import select, text

from models import UserOrm, Model, QuizOrm, QuestionOrm, quiz_question_table
from schemas import *

import os

BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, 'db')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

DB_PATH = os.path.join(DB_DIR, 'fastapi.db')

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")
# engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}", echo=True) # echo=True - все sql в консоль
# engine = create_async_engine("sqlite+aiosqlite:///example//fastapi//db//fastapi.db")
# engine = create_async_engine("sqlite+aiosqlite:///db//fastapi.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)


# expire_on_commit=False отключает истечение (сброс) атрибутов объектов после commit() в SQLAlchemy сессии.
# если True - после комита обращение к любому полю создаст новый запрос, если False -возмет из памяти


class DataRepository:
    @classmethod
    async def create_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.create_all)

    @classmethod
    async def delete_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.drop_all)

    @classmethod
    async def add_test_data(cls):
        async with new_session() as session:
            users = [
                UserOrm(name='user1', age=20),
                UserOrm(name='user2', age=30, phone='123456789'),
                UserOrm(name='user3', age=41, phone='11'),
                UserOrm(name='user4', age=42, phone='22'),
                UserOrm(name='user5', age=43, phone='33'),
                UserOrm(name='user6', age=44),
                UserOrm(name='user7', age=45)
            ]

            session.add_all(users)

            # flush() - используется для синхронизации изменений с базой данных без завершения транзакции
            # проверяет, что операции (вставка, обновление) не вызывают ошибок
            # Если последующие действия в транзакции зависят от предыдущих изменений,
            # flush() делает эти изменения видимыми в рамках текущей сессии
            await session.flush()
            await session.commit()


class UserRepository:

    @classmethod
    async def add_user(cls, user: UserAdd) -> int:
        async with new_session() as session:
            data = user.model_dump()  # -> dict
            user = UserOrm(**data)
            session.add(user)  # не производит операций с БД только с памятью поэтому синхронно
            await session.flush()
            await session.commit()
            return user.id

    @classmethod
    async def get_users(cls, limit, offset) -> list[UserOrm]:
        async with new_session() as session:
            # query = select(UserOrm)
            query = select(UserOrm).limit(limit).offset(offset)

            # query = user_filter.filter(query).limit(limit).offset(offset)
            # query = user_filter.sort(query)
            # query = text(f"SELECT * FROM users WHERE id={id}")

            res = await session.execute(query)
            users = res.scalars().all()
            return users

    @classmethod
    async def get_user(cls, id) -> UserOrm:
        async with new_session() as session:
            query = select(UserOrm).filter(UserOrm.id == id)
            # query = text(f"SELECT * FROM users WHERE id={id}")
            res = await session.execute(query)
            user = res.scalars().first()
            return user


class QuizRepository:
    @classmethod
    async def add_quiz(cls, quiz: QuizAdd) -> int:
        async with new_session() as session:
            data = quiz.model_dump()
            obj = QuizOrm(**data)
            session.add(obj)
            await session.flush()
            await session.commit()
            return obj.id

    @classmethod
    async def get_quizes(cls, limit: int | None = None, offset: int = 0) -> list[QuizOrm]:
        async with new_session() as session:
            query = select(QuizOrm).offset(offset)
            if limit is not None:
                query = query.limit(limit)
            res = await session.execute(query)
            quizes = res.scalars().all()
            return quizes

    @classmethod
    async def get_quiz(cls, id: int) -> QuizOrm | None:
        async with new_session() as session:
            query = select(QuizOrm).filter(QuizOrm.id == id)
            res = await session.execute(query)
            quiz = res.scalars().first()
            return quiz

    @classmethod
    async def get_quiz_questions(cls, id: int) -> list[QuestionOrm]:
        async with new_session() as session:
            query = (
                select(QuestionOrm)
                .join(quiz_question_table, QuestionOrm.id == quiz_question_table.c.question_id)
                .where(quiz_question_table.c.quiz_id == id)
            )
            res = await session.execute(query)
            questions = res.scalars().all()
            return questions

    @classmethod
    async def link_questions(cls, quiz_id: int, question_ids: list[int]) -> None:
        """Привязать существующие вопросы к квизу (перезаписывать связи не будем)."""
        async with new_session() as session:
            quiz = await session.get(QuizOrm, quiz_id)
            if not quiz:
                return

            # Найти все вопросы по переданным id
            query = select(QuestionOrm).where(QuestionOrm.id.in_(question_ids))
            res = await session.execute(query)
            questions = res.scalars().all()

            for q in questions:
                if q not in quiz.questions:
                    quiz.questions.append(q)

            await session.commit()


class QuestionRepository:
    @classmethod
    async def add_question(cls, question: QuestionAdd) -> int:
        async with new_session() as session:
            data = question.model_dump()
            obj = QuestionOrm(**data)
            session.add(obj)
            await session.flush()
            await session.commit()
            return obj.id

    @classmethod
    async def get_questions(cls, limit: int | None = None, offset: int = 0) -> list[QuestionOrm]:
        async with new_session() as session:
            query = select(QuestionOrm).offset(offset)
            if limit is not None:
                query = query.limit(limit)
            res = await session.execute(query)
            questions = res.scalars().all()
            return questions

    @classmethod
    async def get_question(cls, id: int) -> QuestionOrm | None:
        async with new_session() as session:
            query = select(QuestionOrm).filter(QuestionOrm.id == id)
            res = await session.execute(query)
            question = res.scalars().first()
            return question
