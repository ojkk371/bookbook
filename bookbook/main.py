from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
from bookbook.models import mongodb
from bookbook.__about__ import __logo__
from bookbook.models.book import BookModel
from bookbook.book_scraper import NaverBookScraper


LOGO = __logo__
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "북북이"},
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    keyword = q

    if not keyword:
        return templates.TemplateResponse(
            "./index.html",
            {"request": request, "title": "북북이"},
        )
    if await mongodb.engine.find_one(BookModel, BookModel.keyword == keyword):
        books = await mongodb.engine.find(BookModel, BookModel.keyword == keyword)
        return templates.TemplateResponse(
            "./index.html",
            {"request": request, "title": "북북이", "books": books},
        )

    naver_book_scraper = NaverBookScraper()
    books = await naver_book_scraper.search(keyword, 10)
    book_models = []
    for book in books:
        book_model = BookModel(
            keyword=keyword,
            publisher=book["publisher"],
            price=book["price"],
            image=book["image"],
        )
        book_models.append(book_model)
    await mongodb.engine.save_all(book_models)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "북북이", "keyword": q},
    )


@app.on_event("startup")
def on_app_start():
    print(LOGO)
    """start"""
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    """shutdown"""
    mongodb.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
