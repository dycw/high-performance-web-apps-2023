from typing import Any, Iterator, cast
from typing import Any, Iterator

from pymongo import MongoClient
from beartype import beartype
from databases import Database
from fastapi import Body, Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine
from uvicorn import run

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


DATABASE_URL = "sqlite:///./mydata.sqlite3"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()


booklist = Table(
    "booklist",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("title", String(50), unique=True),
    Column("author", String(50)),
    Column("price", Integer),
    Column("publisher", String(50)),
)
metadata.create_all(bind=engine)


async def get_db() -> Any:
    db = Database(DATABASE_URL)
    await db.connect()
    yield db


@beartype
def get_collection() -> Iterator[Any]:
    client = MongoClient()
    yield client["mydata"]["books"]


class Book(BaseModel):
    id: int  # noqa: A003
    title: str
    author: str
    price: int
    publisher: str

    class Config:
        orm_mode = True


@app.post("/books", response_model=Book)
@beartype
async def add_book(*, b1: Book, db: Database = Depends(get_db)) -> str:
    query = booklist.insert().values(
        id=b1.id,
        title=b1.title,
        author=b1.author,
        price=b1.price,
        publisher=b1.publisher,
    )
    await db.execute(query)
    return "Book created successfully"


@app.get("/books/{id}")
@beartype
async def get_book(
    *, id: int, db: Database = Depends(get_db)  # noqa: A002
) -> Book | None:
    query = booklist.select().where(booklist.c.id == id)
    return cast(Book | None, await db.fetch_one(query))


@app.put("/books/{id}")
@beartype
async def update_book(
    *, id: int, new_price: int = Body(), db: Database = Depends(get_db)  # noqa: A002
) -> str:
    query = booklist.update().where(booklist.c.id == id).values(price=new_price)
    await db.execute(query)
    return "Book updated successfully"


@app.delete("/books/{id}")
@beartype
async def delete_book(*, id: int, db: Database = Depends(get_db)) -> str:  # noqa: A002
    query = booklist.delete().where(booklist.c.id == id)
    await db.execute(query)
    return "Book deleted successfully"


if __name__ == "__main__":
    run("main:app", host="127.0.0.1", port=8000, reload=True)
