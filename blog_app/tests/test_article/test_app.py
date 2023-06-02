from fastapi.testclient import TestClient
from blog_app.blog.app import app
import pytest

client = TestClient(app)

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

def test_create_article():
    """
    GIVEN: valid request data
    WHEN: endpoint /create-article/ is called
    THEN: it should return status_code 200 and return article
    """
    body = new_article_body("john@doe.com", "New Article", "Some extra awesome content")
    print("body --------- ", body)

    new_article = create_article(body)
    parse_new_article = new_article.json()
    print("parse_new_article --------- ", parse_new_article)

    assert new_article.status_code == 200
    assert parse_new_article["author"] == body["author"]
    assert parse_new_article["title"] == body["title"]
    assert parse_new_article["content"] == body["content"]

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
def test_create_article_bad_request(data):
    """
    GIVEN request data with invalid values or missing attributes
    WHEN endpoint /create-article/ is called
    THEN it should return status 422 Unprocessable Entity
    """
    response = create_article(data)

    assert response.status_code == 422
    assert response.json() is not None


def test_get_article():
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

def test_list_articles():
    response = client.post("/create-article/", json={
        "author": "jane@doe.com",
        "title": "Article 1",
        "content": "This is article 1"
    })
    assert response.status_code == 200
    data = response.json()
    article_id_1 = data["id"]

    response = client.post("/create-article/", json={
        "author": "john@doe.com",
        "title": "Article 2",
        "content": "This is article 2"
    })
    assert response.status_code == 200
    data = response.json()
    article_id_2 = data["id"]

    response = client.get("/article-list/")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 2
    assert {"id": article_id_1, "author": "jane@doe.com", "title": "Article 1", "content": "This is article 1"} in data
    assert {"id": article_id_2, "author": "john@doe.com", "title": "Article 2", "content": "This is article 2"} in data

