from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
import uvicorn
from routers import default_router, users_router, quizes_router, questions_router
from database import DataRepository as dr


@asynccontextmanager  # реагирует на методы __aenter__() и __aexit__()
async def lifespan(app: FastAPI):
    await dr.create_table()
    await dr.add_test_data()
    print("🔧 База данных и тестовые данные созданы")

    yield
    await dr.delete_table()
    print(" База данных очищена (drop_all)")


app = FastAPI(
    title="Homework 10 API (Eliza)",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(default_router)
app.include_router(users_router)
app.include_router(quizes_router)
app.include_router(questions_router)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
