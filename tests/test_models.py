import uuid
from api.models import AbstractUser, SuperAdmin, Operator, ExchangeRatesRecord, RefreshToken, UserType

import pytest
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


''' AbstractUser models tests'''
# pytest tests/test_models.py -s


def test_abstract_user_set_password(db_session, mocker):
    """ create password for user """
    user = AbstractUser()
    mocker.patch('api.models.validate_password')
    user.set_password("nazca007")
    assert user.password_hash is not None


def test_abstract_user_change_password(db_session, mocker):
    """ set new password and change it """

    user = AbstractUser()
    mocker.patch('api.models.validate_password')
    user.set_password("nazca001")
    password_old = "nazca001"
    password_new = "nazca008"
    user.change_password(password_old, password_new)
    result = user.check_password(password_new)
    assert result == True


def test_abstract_user_change_password_error(db_session, mocker):
    """ invalid old password """

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


''' SuperAdmin models tests'''


def test_abstract_user_cant_create_user(db_session):
    """ User try to create new user - result Error """

    with pytest.raises(Exception):
        user = SuperAdmin(
            is_confirmed=True
        )
        result = user.can_create_user(UserType.User)


def test_abstract_admin_can_create_user(db_session):
    """ Admin can create new user """

    admin = SuperAdmin(
        is_confirmed=True
    )
    result = admin.can_create_user(UserType.SUPER_ADMIN)


def test_abstract_user_can_read(db_session):
    """ Admin can create new user """

    user = SuperAdmin(is_confirmed=True)
    result = user.can_read_user(UserType.USER)


def test_abstract_user_is_not_confirmed(db_session):
    """ User is not confirmed can do nothing - result Error """

    with pytest.raises(Exception):
        user = SuperAdmin(
            is_confirmed=False)
        result = user.can_read_user(UserType.USER)


def test_abstract_user_can_edit_user(db_session):
    """ Admin can create new user """

    user = SuperAdmin(is_confirmed=True)
    result = user.can_edit_user(UserType.USER)


''' Operator models tests'''


def test_operator_cant_create_user(db_session):
    """ Operator can't create some user """

    user_operator = Operator(is_confirmed=True)
    result = user_operator.can_create_user(UserType.OPERATOR)
    assert result == False


def test_operator_can_read_user(db_session):
    """ Operator can't read some user only self """

    user_operator = Operator(is_confirmed=True)
    result_1 = user_operator.can_read_user(user_operator)
    result_2 = user_operator.can_read_user(UserType.USER)

    assert result_1 == True
    assert result_2 == False


def test_operator_can_edit_user(db_session):
    """ Operator can't edit some user only self """

    user_operator = Operator(is_confirmed=True)
    result_1 = user_operator.can_edit_user(user_operator)
    result_2 = user_operator.can_edit_user(UserType.USER)

    assert result_1 == True
    assert result_2 == False


def test_create_refresh_token(db_session):
    """ Create some token value """

    user_id_uuid = uuid.uuid4()
    refresh_token = RefreshToken(user_id=user_id_uuid, value='new_token')
    assert refresh_token.value == 'new_token'


def test_exchange_rates_record(db_session):
    """ Create exchange_rates object """

    user = AbstractUser()
    exchange = ExchangeRatesRecord(actor_id=user.user_id, rate=10.05)

    assert exchange.rate == 10.05
    assert exchange.actor_id == user.user_id
