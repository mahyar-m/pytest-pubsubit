import unittest
import pytest

from pytest_pubsubit.pubsub_helper import PubSubHelper
from pytest_pubsubit.pubsub_manager import PubSubManager


class PubSubTestCase(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def init(self, psm_function_fixture: PubSubManager) -> None:
        self.pubsub_manager = psm_function_fixture

    def assertMessageExist(self, project, subscription, expected_message_data, max_messages=100) -> None:
        messages = PubSubHelper.sync_pull(self.pubsub_manager.get_subscriber_client(), project=project,
                                          subscription=subscription, max_messages=max_messages, is_ack=False)

        for message in messages:
            if message.data == expected_message_data:
                return

        raise AssertionError("Message doesn't exist")

    def assertTopicExist(self, project, expected_topic) -> None:
        self.assertTrue(
            PubSubHelper.is_topic_exist(self.pubsub_manager.get_publisher_client(), project, expected_topic),
            "Topic '{}' in project '{}' is not exist".format(expected_topic, project))

    def assertTopicNotExist(self, project, expected_topic) -> None:
        self.assertFalse(
            PubSubHelper.is_topic_exist(self.pubsub_manager.get_publisher_client(), project, expected_topic),
            "Topic '{}' in project '{}' is exist".format(expected_topic, project))

    def assertNoTopicExist(self, project) -> None:
        topic_count = PubSubHelper.topic_count(self.pubsub_manager.get_publisher_client(), project)
        self.assertEqual(0, topic_count, "There is still {} topics exist".format(topic_count))

    def assertSubscriptionExist(self, project, expected_subscription) -> None:
        self.assertTrue(
            PubSubHelper.is_subscription_exist(self.pubsub_manager.get_subscriber_client(), project,
                                               expected_subscription),
            "Subscription '{}' in project '{}' is not exist".format(expected_subscription, project))

    def assertSubscriptionNotExist(self, project, expected_subscription) -> None:
        self.assertFalse(
            PubSubHelper.is_subscription_exist(self.pubsub_manager.get_subscriber_client(), project,
                                               expected_subscription),
            "Subscription '{}' in project '{}' is exist".format(expected_subscription, project))

    def assertNoSubscriptionExist(self, project) -> None:
        subscription_count = PubSubHelper.subscription_count(self.pubsub_manager.get_subscriber_client(), project)
        self.assertEqual(0, subscription_count, "There is still {} subscriptions exist".format(subscription_count))
