from django.urls import reverse
from django.test.client import Client
import pytest
from api.models import AbstractUser, ExchangeRatesRecord, RefreshToken, SuperAdmin, UserType, Operator

import pytest
from lamb.db import DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session



def test_ping():
    client = Client()
    response = client.get(reverse("api:ping"), content_type="application/json")
    assert response.status_code == 200
    assert response.json() == {"response": "pong"}


def test_auth_bad_creds():
    client = Client()
    response = client.post(
        reverse("api:auth"),
        content_type="application/json",
        data={
            "engine": "email",
            "credentials": {
                "email": "some@email",
                "password": "StrongPassword",
            },
        },
    )
    assert response.status_code == 401


@pytest.fixture(scope='session')
def db_engine(request):
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    engine_ = create_engine("postgresql://app_user:LC50UD2nTh@localhost:55432/app_core", echo=True)
    yield engine_
    engine_.dispose()


@pytest.fixture(scope='session')
def db_session_factory(db_engine):
    """returns a SQLAlchemy scoped session factory"""
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope='function')
def db_session(db_session_factory):
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    session_ = db_session_factory()
    yield session_

    session_.rollback()
    session_.close()


def test_abstract_user_set_password(db_session, mocker):
    user = AbstractUser()
    mocker.patch('api.models.validate_password')
    user.set_password("nazca007")
    assert user.password_hash is not None

