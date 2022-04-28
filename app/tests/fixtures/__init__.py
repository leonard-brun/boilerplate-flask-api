import pytest

from boilerplate import create_app, db


@pytest.fixture(scope="session")
def app():
    """Create app and init db"""
    app = create_app("test")
    with app.app_context():
        db.create_all()
    return app


@pytest.fixture
def client(app):
    """Create session and rollback after each test"""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    init_session = db.session
    db.session = session

    with app.test_client() as client:
        with app.app_context():
            yield client

    transaction.rollback()
    connection.close()
    session.remove()
    db.session = init_session
