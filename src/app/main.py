from fastapi import FastAPI, Form, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base
from uvicorn import run


class Product(BaseModel):
    prod_id: int
    prod_name: str
    price: float
    stock: int

    class Config:
        orm_mode = True


Base = declarative_base()


class ProductORM(Base):
    __tablename__ = "products"

    prod_id = Column(Integer, primary_key=True, nullable=False)
    prod_name = Column(String(63), unique=True)
    price = Column(Float)
    stock = Column(Integer)


product_alchemy = ProductORM(prod_id=1, prod_name="Ceiling Fan", price=2000, stock=50)
product = Product.from_orm(product_alchemy)
product_alchemy_again = ProductORM(**product.dict())


templates = Jinja2Templates(directory="templates")


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/employee/{name}/{salary}")
async def employee_salary(*, request: Request, name: str, salary: int) -> Response:
    data = {"name": name, "salary": salary}
    return templates.TemplateResponse(
        "employee.html", {"request": request, "data": data}
    )


@app.get("/profile")
async def info(*, request: Request) -> Response:
    data = {"name": "Ronie", "langs": ["Python", "Java", "PHP", "Swift", "Ruby"]}
    return templates.TemplateResponse(
        "profile.html", {"request": request, "data": data}
    )


@app.get("/testjs/{name}")
async def jsdemo(*, request: Request, name: str) -> Response:
    data = {"name": name}
    return templates.TemplateResponse(
        "static-js.html", {"request": request, "data": data}
    )


@app.get("/img/")
async def show_image(*, request: Request) -> Response:
    return templates.TemplateResponse("static-img.html", {"request": request})


@app.get("/form/")
async def form(*, request: Request) -> Response:
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/form/")
async def getform(
    *, name: str = Form(...), add: str = Form(...), post: str = Form(...)
) -> dict[str, str]:
    return {"Name": name, "Address": add, "Post applied": post}


if __name__ == "__main__":
    run("main:app", host="127.0.0.1", port=8000, reload=True)
