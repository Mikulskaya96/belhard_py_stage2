from fastapi import APIRouter, HTTPException, Depends, Query

from schemas import *
from database import UserRepository as ur, QuizRepository as qr, QuestionRepository as qsr

# pip install fastapi_filter
from fastapi_filter import FilterDepends

# Отдельные роутеры для разных разделов API
default_router = APIRouter()

users_router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)

quizes_router = APIRouter(
    prefix="/quizes",
    tags=["Квизы"],
)

questions_router = APIRouter(
    prefix="/questions",
    tags=["Вопросы"],
)


@default_router.get("/", tags=["API V1"])
async def index() -> dict[str, str]:
    """Простейший health-check, чтобы понять, что API живое."""
    return {
        "data": "ok",
        "message": "Homework 10 FastAPI is running",
    }


# ответ в виде одиночного списка
@users_router.get("")
async def users_get(
        limit: int = Query(ge=1, lt=10, default=3),
        offset: int = Query(ge=0, default=0),
        # user_filter: UserFilter = FilterDepends(UserFilter)
) -> dict[str, int | list[User]]:
    # users =   await ur.get_users(limit, offset, user_filter)
    users = await ur.get_users(limit, offset)

    # return users

    # с развернутым ответом
    return {"data": users, "limit": limit, "offset": offset}


@users_router.get("/u2")
async def users_get2() -> dict[str, list[User] | str]:
    users = await ur.get_users()
    return {"status": "ok", "data": users}


@users_router.get("/{id}")
async def user_get(id: int) -> User:
    user = await ur.get_user(id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="Пользователь не найден")
    # или return {'err':"User not found, ..."} # но тогда get_user(id) -> User | dict[str,str]


@users_router.post("")
async def add_user(user: UserAdd = Depends()) -> UserId:
    id = await ur.add_user(user)
    return {"id": id}


@quizes_router.get("")
async def quizes_get(
    limit: int = Query(ge=1, lt=50, default=10),
    offset: int = Query(ge=0, default=0),
) -> dict[str, list[Quiz] | int]:
    """Получить список квизов с пагинацией."""
    quizes = await qr.get_quizes(limit=limit, offset=offset)
    return {"items": quizes, "limit": limit, "offset": offset}


@quizes_router.post("")
async def quizes_add(quiz: QuizAdd) -> QuizId:
    """Создать новый квиз."""
    quiz_id = await qr.add_quiz(quiz)
    return {"id": quiz_id}


@quizes_router.get("/{id}")
async def quiz_get(id: int) -> Quiz:
    """Получить один квиз по id."""
    quiz = await qr.get_quiz(id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Квиз не найден")
    return quiz


@quizes_router.get("/{id}/questions")
async def quiz_questions(id: int) -> dict[str, list[Question] | int]:
    """
    Вариант 2 из задания:
    вернуть список вопросов, привязанных к указанному квизу.
    """
    quiz = await qr.get_quiz(id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Квиз не найден")

    questions = await qr.get_quiz_questions(id)
    return {"quiz_id": id, "questions": questions}


@quizes_router.post("/{id}/link")
async def quiz_link_questions(id: int, link: QuizQuestionsLink) -> dict[str, str]:
    """
    Привязать существующие вопросы к квизу
    (по списку идентификаторов вопросов).
    """
    quiz = await qr.get_quiz(id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Квиз не найден")

    await qr.link_questions(id, link.question_ids)
    return {"status": "ok"}


# --------- ВОПРОСЫ ---------


@questions_router.get("")
async def questions_get(
    limit: int = Query(ge=1, lt=100, default=20),
    offset: int = Query(ge=0, default=0),
) -> dict[str, list[Question] | int]:
    """Получить список вопросов с пагинацией."""
    questions = await qsr.get_questions(limit=limit, offset=offset)
    return {"items": questions, "limit": limit, "offset": offset}


@questions_router.post("")
async def questions_add(question: QuestionAdd) -> QuestionId:
    """Создать новый вопрос."""
    q_id = await qsr.add_question(question)
    return {"id": q_id}


@questions_router.get("/{id}")
async def question_get(id: int) -> Question:
    """Получить один вопрос по id."""
    question = await qsr.get_question(id)
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    return question

# пример развернутого ответа
#     {
# "items": [...],
# "total": 100,
# "page": 1,
# "size": 10,
# "pages": 10
# }

# Или с ссылками:

# {
# "items": [...],
# "total": 100,
# "page": 1,
# "size": 10,
# "pages": 10,
# "links": {
# "next": "http://api.example.com/items?page=2",
# "prev": null,
# "first": "http://api.example.com/items?page=1",
# "last": "http://api.example.com/items?page=10"
# }
# }