from fastapi import FastAPI, Path
from pydantic import BaseModel
from blog_app.blog.commands import CreateArticleCommand
from blog_app.blog.queries import GetArticleByIDQuery, ListArticlesQuery

app = FastAPI()

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
