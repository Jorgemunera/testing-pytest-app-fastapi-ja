import os
import tempfile

import pytest

from blog_app.blog.models import Article

@pytest.fixture(autouse=True)
def database():
    _, file_name = tempfile.mkstemp()
    os.environ["DATABASE_NAME"] = file_name
    Article.create_table(database_name=file_name)

    # Asegurándote de que la base de datos está vacía antes de cada prueba
    Article.delete_all()

    yield