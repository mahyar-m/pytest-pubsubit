from __future__ import annotations

import json
import os

from _pytest.fixtures import FixtureRequest
from google.pubsub_v1 import PublisherClient, SubscriberClient

from pytest_pubsubit.pubsub_helper import PubSubHelper
from google.cloud import pubsub_v1


class PubSubManager:
    """Class to manage the creation of the test PubSub topics and subscriptions"""

    def __init__(self, request: FixtureRequest) -> None:
        """Initialize the class."""

        self.request = request
        self.publisher_client = None
        self.project = None
        self.topics_subscriptions = None
        self.global_fixtures_path = None

    def get_publisher_client(self) -> PublisherClient:
        """Return a connection"""

        return self.publisher_client

    def get_subscriber_client(self) -> SubscriberClient:
        """Return a connection"""

        return pubsub_v1.SubscriberClient()

    def _init_config(self) -> None:
        """Initialize the config from pytest options"""

        for option in ['project', 'topics_subscriptions', 'global_fixtures_path']:
            option_name = 'pubsubit_' + option
            setattr(self, option, self.request.config.getoption(option_name) or self.request.config.getini(option_name))

        if self.topics_subscriptions:
            self.topics_subscriptions = json.loads(self.topics_subscriptions)

    def _setup(self) -> None:
        """Setup the test topics"""

        self._init_config()

        self.publisher_client = pubsub_v1.PublisherClient()
        PubSubHelper.delete_all_subscriptions(self.get_subscriber_client(), self.project)
        PubSubHelper.delete_all_topics(self.publisher_client, self.project)
        for topic, subscriptions in self.topics_subscriptions.items():
            PubSubHelper.create_topic(self.publisher_client, self.project, topic)
            for subscription in subscriptions:
                PubSubHelper.create_subscription(self.get_subscriber_client(), self.project, topic, subscription)

    def _teardown(self) -> None:
        """Teardown the test topics"""

        PubSubHelper.delete_all_subscriptions(self.get_subscriber_client(), self.project)
        PubSubHelper.delete_all_topics(self.publisher_client, self.project)

    def __enter__(self) -> PubSubManager:
        self._setup()
        return self

    def __exit__(self, *exc_details) -> None:
        self._teardown()

    def exec_json_file(
            self,
            json_file_path: str,
            location: str = 'local',
            request: FixtureRequest = None,
            local_path: str = None,
            global_path: str = None
    ) -> None:
        """Execute a json file"""

        if not global_path:
            global_path = os.path.join(self.global_fixtures_path)

        if location == 'local':
            if not local_path:
                local_path = os.path.join(request.fspath.dirname, 'fixtures', 'pubsub')
            json_file_path = os.path.join(local_path, json_file_path)
        elif location == 'global':
            json_file_path = os.path.join(global_path, json_file_path)
        elif location == 'relative':
            json_file_path = os.path.join(request.fspath.dirname, json_file_path)

        if not os.path.isfile(json_file_path):
            return

        PubSubHelper.exec_json_file(self.get_publisher_client(), self.get_subscriber_client(), json_file_path,
                                    global_path)
