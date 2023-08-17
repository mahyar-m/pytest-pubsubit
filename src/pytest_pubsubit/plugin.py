import pytest

from _pytest.fixtures import FixtureRequest
from pytest_pubsubit.pubsub_manager import PubSubManager

pytest_options = [
    {
        'name': 'pubsubit_project',
        'option': '--pubsubit-project',
        'default': '127.0.0.1',
        'help': '',
    },
    {
        'name': 'pubsubit_topics_subscriptions',
        'option': '--pubsubit-topics-subscriptions',
        'default': '',
        'help': '',
    },
    {
        'name': 'pubsubit_global_fixtures_path',
        'option': '--pubsubit-global-fixtures-path',
        'default': 'tests/integration/fixtures/pubsub',
        'help': '',
    },
]


def pytest_addoption(parser) -> None:
    """Configure for pytest-pubsubit"""

    for option in pytest_options:
        parser.addini(
            name=option['name'],
            default=option['default'],
            help=option['help'],
        )

        parser.addoption(
            option['option'],
            action='store',
            dest=option['name'],
        )


@pytest.fixture(scope="session")
def psm_session_fixture(request: FixtureRequest) -> PubSubManager:
    with PubSubManager(request) as pubsub_manager:
        yield pubsub_manager


@pytest.fixture(scope="class")
def psm_class_fixture(psm_session_fixture: PubSubManager, request: FixtureRequest) -> PubSubManager:
    psm_session_fixture.exec_json_file('setup_class.json', location='local', request=request)
    yield psm_session_fixture
    psm_session_fixture.exec_json_file('teardown_class.json', location='local', request=request)


@pytest.fixture(scope="function")
def psm_function_fixture(psm_class_fixture: PubSubManager, request: FixtureRequest) -> PubSubManager:
    psm_class_fixture.exec_json_file('setup_method.json', location='local', request=request)
    yield psm_class_fixture
    psm_class_fixture.exec_json_file('teardown_method.json', location='local', request=request)
