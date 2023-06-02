from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError
from blog_app.blog.commands import AlreadyExists, CreateArticleCommand
from blog_app.blog.queries import GetArticleByIDQuery, ListArticlesQuery
from blog_app.blog.models import NotFound
from blog_app.blog.models import Article

app = FastAPI()
Article.create_table()

class ArticleIn(BaseModel):
    author: str
    title: str
    content: str

class ArticleOut(BaseModel):
    id: str
    author: str
    title: str
    content: str


@app.post("/create-article/", response_model=ArticleOut)
async def create_article(article: ArticleIn):
    cmd = CreateArticleCommand(**article.dict())
    return cmd.execute().dict()

@app.get("/article/{article_id}/", response_model=ArticleOut)
async def get_article(article_id: str):
    query = GetArticleByIDQuery(id=article_id)
    return query.execute().dict()

@app.get("/article-list/", response_model=list[ArticleOut])
async def list_articles():
    query = ListArticlesQuery()
    records = [record.dict() for record in query.execute()]
    return records




@app.exception_handler(RequestValidationError)
async def handler_validation_exception(request, exc: RequestValidationError):
    response = exc.errors()
    return JSONResponse(status_code = 422, content = jsonable_encoder(response))

@app.exception_handler(ValidationError)
async def handler_validation_error(request, exc: ValidationError):
    response = exc.errors()
    return JSONResponse(status_code=422, content= jsonable_encoder(response))

@app.exception_handler(AlreadyExists)
async def handler_validation_error(request: Request, exc: AlreadyExists):
    response = exc
    return JSONResponse(status_code=200, content= jsonable_encoder(response))

@app.exception_handler(NotFound)
async def handler_validation_error(request: Request, exc: NotFound):
    response = exc
    return JSONResponse(status_code=404, content= jsonable_encoder(response))