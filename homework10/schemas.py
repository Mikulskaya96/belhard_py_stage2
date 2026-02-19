from pydantic import BaseModel, ConfigDict


class UserAdd(BaseModel):
    """Данные, которые приходят от клиента при создании пользователя."""

    name: str
    age: int
    phone: str | None = None


class User(UserAdd):
    """Полная модель пользователя, которую возвращает API."""

    id: int

    # возможность сбора модели из атрибутов объекта (как правило из ORM)
    # Без этого параметра Pydantic ожидал бы словарь, а не объект с атрибутами.
    model_config = ConfigDict(from_attributes=True)


class UserId(BaseModel):
    """Ответ с идентификатором только что созданного пользователя."""

    id: int


class QuizAdd(BaseModel):
    """Данные для создания нового квиза."""

    title: str


class Quiz(QuizAdd):
    """Полная модель квиза."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class QuizId(BaseModel):
    """Ответ с идентификатором созданного квиза."""

    id: int


class QuestionAdd(BaseModel):
    """Данные для создания вопроса."""

    text: str
    answer: str


class Question(QuestionAdd):
    """Полная модель вопроса."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class QuestionId(BaseModel):
    """Ответ с идентификатором созданного вопроса."""

    id: int


class QuizQuestionsLink(BaseModel):
    """Связать квиз с существующими вопросами."""

    question_ids: list[int]