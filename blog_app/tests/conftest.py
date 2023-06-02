import os
import tempfile

import pytest

from blog_app.blog.models import Article

@pytest.fixture(autouse=True)
def database():
    # Antes de cada prueba creamos una base de datos
    _, file_name = tempfile.mkstemp()
    os.environ["DATABASE_NAME"] = file_name
    Article.create_table(database_name=file_name)

    yield

    # despues de cada prueba vaciamos su contenido
    Article.delete_all()
