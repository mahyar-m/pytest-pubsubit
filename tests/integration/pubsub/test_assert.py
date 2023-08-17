from pytest_pubsubit.pubsub_helper import PubSubHelper
from pytest_pubsubit.pubsub_test_case import PubSubTestCase


class TestAssert(PubSubTestCase):

    def test_assertTopicExist(self):
        self.assertTopicExist(self._get_project(), 'test-topic')
        self.assertTopicExist(self._get_project(), 'test-topic-2')

    def test_assertTopicNotExist(self):
        self.assertTopicNotExist(self._get_project(), 'test-topic-not-exist')

    def test_assertNoTopicExist(self):
        project = 'test-project-with-no-topic'
        self.assertNoTopicExist(project)

    def test_assertSubscriptionExist(self):
        self.assertSubscriptionExist(self._get_project(), 'test-subscription')
        self.assertSubscriptionExist(self._get_project(), 'test-subscription-1')
        self.assertSubscriptionExist(self._get_project(), 'test-subscription-2')
        self.assertSubscriptionExist(self._get_project(), 'test-subscription-3')

    def test_assertSubscriptionNotExist(self):
        self.assertSubscriptionNotExist(self._get_project(), 'test-subscription-not-exist')

    def test_assertNoSubscriptionExist(self):
        project = 'test-project-with-no-subscription'
        self.assertNoSubscriptionExist(project)

    def test_assertMessageExist(self):
        project = self._get_project()
        topic = 'test-topic'
        subscription = 'test-subscription'
        message_data = 'test-data'.encode("utf-8")

        PubSubHelper.publish_message(self.pubsub_manager.get_publisher_client(), project, topic, message_data)

        self.assertMessageExist(project, subscription, message_data)

    def test_class_level_message_exist(self):
        project = self._get_project()
        subscription = 'test-subscription'
        message_data = 'class-level-data-1'.encode("utf-8")

        self.assertMessageExist(project, subscription, message_data)

    def test_method_level_message_exist(self):
        project = self._get_project()
        subscription = 'test-subscription'
        message_data = 'method-level-data-1'.encode("utf-8")

        self.assertMessageExist(project, subscription, message_data)

    def _get_project(self):
        return self.pubsub_manager.project
