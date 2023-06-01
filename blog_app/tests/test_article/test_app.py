from fastapi.testclient import TestClient
from blog_app.blog.app import app

client = TestClient(app)

def test_create_article():
    response = client.post("/create-article/", json={
        "author": "john@doe.com",
        "title": "New Article",
        "content": "Some extra awesome content"
    })
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["author"] == "john@doe.com"
    assert data["title"] == "New Article"
    assert data["content"] == "Some extra awesome content"

def test_get_article():
    response = client.post("/create-article/", json={
        "author": "jane@doe.com",
        "title": "Another Article",
        "content": "This is another article"
    })
    assert response.status_code == 200
    data = response.json()
    article_id = data["id"]

    response = client.get(f"/article/{article_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == article_id
    assert data["author"] == "jane@doe.com"
    assert data["title"] == "Another Article"
    assert data["content"] == "This is another article"

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
