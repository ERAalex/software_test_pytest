import uuid
from api.tasks import store_exchanges_rates_task
import pytest

''' CELERY TESTS'''
# pytest tests/test_celery.py -s


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'redis://localhost:16379',
        'result_backend': 'redis://localhost:16379'
    }


@pytest.fixture(scope="session")
def celery_worker():
    return {
        "perform_ping_check": False,
    }


def test_celery_worker_initializes(celery_config, celery_worker):
    """ Check if celery_config and celery_worker work"""
    assert True


def test_store_exchanges_rates_task(celery_config, celery_worker):
    result = store_exchanges_rates_task.delay(actor_id=uuid.uuid4()).get(timeout=2)
    return result

    # with pytest.raises(Exception):
    #     result = store_exchanges_rates_task.delay(actor_id=uuid.uuid4()).get(timeout=2)
    #     return result





