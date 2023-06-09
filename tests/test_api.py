from django.urls import reverse
from django.test.client import Client

from faker import Faker
fake = Faker()

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


''' API VIEW TESTS'''
# pytest tests / test_api.py - s


def test_app_version_get():
    client = Client()
    response = client.get(reverse("api:app_versions"), content_type="application/json")
    assert response.status_code == 200


def test_ping_view_get():
    ''' try to recive 200 and json response - pong '''
    client = Client()
    response = client.get(reverse("api:ping"), content_type="application/json")
    assert response.json() == {'response': 'pong'}


def test_handbooks_list():
    ''' recive status 200 and list with token's data '''
    client = Client()
    response = client.get(reverse("api:handbooks_list"), content_type="application/json")
    data = response.json()
    assert response.status_code == 200
    assert type(data['configs']) == list
    # we can return result to see what we get
    return data['configs']


def test_handbooks_item_list():

    client = Client()
    # let's use interesting library - Fake. But we need to delete space between name & surname
    handbook_name = fake.name().replace(' ', '_')
    url_path = reverse("api:handbooks_item_list",
                                  kwargs={"handbook_name": handbook_name})
    response = client.get(url_path, content_type="application/json")

    assert response.status_code == 404

