import lamb
from django.urls import reverse
from django.test.client import Client
import pytest
from api.models import AbstractUser, ExchangeRatesRecord, RefreshToken, SuperAdmin, UserType, Operator

import pytest
from lamb.db import DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


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
    ''' create password for user '''
    user = AbstractUser()
    mocker.patch('api.models.validate_password')
    user.set_password("nazca007")
    assert user.password_hash is not None


def test_abstract_user_change_password(db_session, mocker):
    ''' set new password and change it '''
    user = AbstractUser()
    mocker.patch('api.models.validate_password')
    user.set_password("nazca001")
    password_old = "nazca001"
    password_new = "nazca008"
    user.change_password(password_old, password_new)
    result = user.check_password(password_new)
    assert result == True


def test_abstract_user_change_password_error(db_session, mocker):
    ''' invalid old password '''
    with pytest.raises(Exception):
        user = AbstractUser()
        mocker.patch('api.models.validate_password')
        user.set_password("nazca001")
        password_old = "nazca004"
        password_new = "nazca008"
        result = user.change_password(password_old, password_new)


def test_abstract_user_validate_name(db_session):
    with pytest.raises(Exception):
        user = AbstractUser(
            email='some_wrong_email')
        db_session.add(user)
        db_session.commit()


def test_abstract_user_can_create(db_session):
    with pytest.raises(Exception):
        user = AbstractUser(
            email='some_wrong_email')
        db_session.add(user)
        db_session.commit()


