from fastapi.testclient import TestClient
from blog_app.blog.app import app
import pytest
import requests

client = TestClient(app)
DOMAIN = "http://localhost:3000"

def new_article_body(author, title, content):
    return {
        "author": author,
        "title": title,
        "content": content
    }

def create_article(body):
    return client.post("/create-article/", json=body)

def get_article(article_id):
    return client.get(f"/article/{article_id}/")

def get_list_articles():
    return client.get("/article-list/")

class TestPostMethod:
    def test_create_article(self):
        """
        GIVEN: valid request data
        WHEN: endpoint /create-article/ is called
        THEN: it should return status_code 200 and return article
        """
        body = new_article_body("john@doe.com", "New Article", "Some extra awesome content")

        new_article = create_article(body)
        parse_new_article = new_article.json()

        assert new_article.status_code == 200
        assert parse_new_article["author"] == body["author"]
        assert parse_new_article["title"] == body["title"]
        assert parse_new_article["content"] == body["content"]

class TestGetMethods:
    @pytest.mark.parametrize(
        "data",
        [
            {
                "author": "John Doe",
                "title": "New Article",
                "content": "Some extra awesome content"
            },
            {
                "author": "John Doe",
                "title": "New Article",
            },
            {
                "author": "John Doe",
                "title": None,
                "content": "Some extra awesome content"
            }
        ]
    )
    def test_create_article_bad_request(self, data):
        """
        GIVEN request data with invalid values or missing attributes
        WHEN endpoint /create-article/ is called
        THEN it should return status 422 Unprocessable Entity
        """
        response = create_article(data)

        assert response.status_code == 422
        assert response.json() is not None


    def test_get_article(self):
        """
        GIVEN an article in database
        WHEN endpoint /article/{article_id}/" is called
        THEN it should return status 200 and the article
        """
        body = new_article_body("jane@doe.com", "Another Article", "This is another article")
        new_article = create_article(body)
        parse_new_article = new_article.json()
        assert new_article.status_code == 200

        article_id = parse_new_article["id"]

        article = get_article(article_id)
        parse_article = article.json()
        assert article.status_code == 200

        assert parse_article["id"] == parse_new_article["id"]
        assert parse_article["author"] == body["author"]
        assert parse_article["title"] == body["title"]
        assert parse_article["content"] == body["content"]

    def test_list_articles(self):
        """
        GIVEN two articles in database
        WHEN endpoint /article-list/" is called
        THEN it should return status 200 and the article list with two elements
        """
        body1 = new_article_body("jane@doe.com", "Article 1", "This is article 1")
        new_article = create_article(body1)
        assert new_article.status_code == 200

        parse_new_article = new_article.json()

        body2 = new_article_body("jane@doe.com", "Article 2", "This is article 2")
        new_article_2 = create_article(body2)
        assert new_article_2.status_code == 200
        parse_new_article_2 = new_article_2.json()

        get_articles = get_list_articles()
        assert get_articles.status_code == 200
        parse_get_articles = get_articles.json()

        assert isinstance(parse_get_articles, list)
        assert len(parse_get_articles) >= 2
        assert parse_new_article in parse_get_articles
        assert parse_new_article_2 in parse_get_articles


@pytest.mark.e2e
def test_create_list_get():
    body = new_article_body("john@doe.com", "New Article", "Some extra awesome content")
    new_article = requests.post(DOMAIN+"/create-article/", json=body)
    assert new_article.status_code == 200

    get_articles = requests.get(DOMAIN+"/article-list")

    parse_get_articles = get_articles.json()

    get_one_article = requests.get(DOMAIN+f"/article/{parse_get_articles[0]['id']}/")

    assert get_one_article.status_code == 200
