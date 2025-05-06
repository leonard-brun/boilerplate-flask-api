import pytest
from sqlalchemy.orm import sessionmaker, scoped_session
from boilerplate import create_app, db


@pytest.fixture(scope="session")
def app():
    app = create_app("test")
    with app.app_context():
        db.create_all()
        yield app
        db.session.close()
        db.drop_all()


@pytest.fixture(scope="function", autouse=True)
def client(app):
    connection = db.engine.connect()

    trans = connection.begin()
    session_factory = sessionmaker(bind=connection)
    session = scoped_session(session_factory)
    init_session = db.session

    session.begin_nested()
    db.session = session

    with app.test_client() as client:
        yield client

    session.close()
    trans.rollback()
    connection.close()
    session.remove()
    db.session = init_session
