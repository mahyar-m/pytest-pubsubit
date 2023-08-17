import json
import time
from pathlib import Path

from google.api_core import retry
from google.api_core.exceptions import AlreadyExists
from google.protobuf.timestamp_pb2 import Timestamp


class PubSubHelper:

    def __init__(self) -> None:
        """Initialize the class."""

        pass

    @staticmethod
    def delete_all_topics(publisher_client, project) -> None:
        project_path = publisher_client.common_project_path(project)

        for topic_path in publisher_client.list_topics(project=project_path):
            publisher_client.delete_topic(topic=topic_path.name)

    @staticmethod
    def create_topic(publisher_client, project, topic) -> None:
        topic_path = publisher_client.topic_path(project, topic)
        try:
            publisher_client.create_topic(name=topic_path)
        except AlreadyExists:
            pass

    @staticmethod
    def is_topic_exist(publisher_client, project, topic) -> bool:
        topic_path = publisher_client.topic_path(project, topic)
        project_path = publisher_client.common_project_path(project)

        for existing_topic_path in publisher_client.list_topics(project=project_path):
            if topic_path == existing_topic_path.name:
                return True

        return False

    @staticmethod
    def topic_count(publisher_client, project) -> int:
        project_path = publisher_client.common_project_path(project)

        return len(list(publisher_client.list_topics(project=project_path)))

    @staticmethod
    def create_subscription(subscriber_client, project, topic, subscription) -> None:
        topic_path = subscriber_client.topic_path(project, topic)
        subscription_path = subscriber_client.subscription_path(project, subscription)
        try:
            with subscriber_client:
                subscriber_client.create_subscription(name=subscription_path, topic=topic_path)
        except AlreadyExists:
            pass

    @staticmethod
    def delete_all_subscriptions(subscriber_client, project) -> None:
        project_path = subscriber_client.common_project_path(project)

        with subscriber_client:
            for subscription in subscriber_client.list_subscriptions(project=project_path):
                subscriber_client.delete_subscription(subscription=subscription.name)

    @staticmethod
    def sync_pull(subscriber_client, project="", subscription="", max_messages=1, return_immediately=True,
                  deadline=300, is_ack=True) -> []:
        subscription_path = subscriber_client.subscription_path(project, subscription)
        with subscriber_client:
            response = subscriber_client.pull(subscription=subscription_path, return_immediately=return_immediately,
                                              max_messages=max_messages, retry=retry.Retry(deadline=deadline))

            received_messages = []
            ack_ids = []
            for received_message in response.received_messages:
                received_messages.append(received_message.message)
                ack_ids.append(received_message.ack_id)

            if is_ack and ack_ids:
                subscriber_client.acknowledge(subscription=subscription_path, ack_ids=ack_ids)

            elif ack_ids:
                subscriber_client.modify_ack_deadline(subscription=subscription_path, ack_ids=ack_ids,
                                                      ack_deadline_seconds=0)
        return received_messages

    @staticmethod
    def is_subscription_exist(subscriber_client, project, subscription) -> bool:
        project_path = subscriber_client.common_project_path(project)
        subscription_path = subscriber_client.subscription_path(project, subscription)

        with subscriber_client:
            for subscription in subscriber_client.list_subscriptions(project=project_path):
                if subscription_path == subscription.name:
                    return True

        return False

    @staticmethod
    def subscription_count(subscriber_client, project) -> int:
        project_path = subscriber_client.common_project_path(project)

        with subscriber_client:
            return len(list(subscriber_client.list_subscriptions(project=project_path)))

    @staticmethod
    def publish_message(publisher_client, project, topic, message_data) -> None:
        topic_path = publisher_client.topic_path(project, topic)
        future = publisher_client.publish(topic_path, message_data)
        message_id = future.result()

        return message_id

    @staticmethod
    def ack_all_messages(subscriber_client, project, subscription) -> None:
        PubSubHelper.sync_pull(subscriber_client, project=project,
                               subscription=subscription, max_messages=100, is_ack=True)

    @staticmethod
    def seek_to_end(subscriber_client, project, subscription) -> None:
        # This will take some time to apply so not a good way to ack all messages
        subscription_path = subscriber_client.subscription_path(project, subscription)

        timestamp = Timestamp()
        timestamp.GetCurrentTime()

        with subscriber_client:
            subscriber_client.seek(
                request={
                    "subscription": subscription_path,
                    "time": timestamp,
                }
            )

    @staticmethod
    def exec_json_file(publisher_client, subscriber_client, json_file_path, global_path):
        if not Path(json_file_path).is_file():
            raise ValueError('{} file is not exist'.format(json_file_path))

        with open(json_file_path) as f:
            commands = json.load(f)

        for command in commands:
            if command['action'] == 'publish':
                PubSubHelper.publish_message(publisher_client, command['project'], command['topic'],
                                             command['data'].encode("utf-8"))
            elif command['action'] == 'ack_all_messages':
                PubSubHelper.ack_all_messages(subscriber_client, command['project'], command['subscription'])

    @staticmethod
    def save_snapshot(subscriber_client, project, subscription):
        snapshot = "snapshot_{}".format(time.time_ns())
        subscription_path = subscriber_client.subscription_path(project, subscription)
        snapshot_path = subscriber_client.snapshot_path(project, snapshot)

        with subscriber_client:
            subscriber_client.create_snapshot(
                request={
                    "name": snapshot_path,
                    "subscription": subscription_path,
                }
            )

        return snapshot

    @staticmethod
    def restore_snapshot(subscriber_client, project, subscription, snapshot):
        subscription_path = subscriber_client.subscription_path(project, subscription)
        snapshot_path = subscriber_client.snapshot_path(project, snapshot)

        subscriber_client.seek(
            request={
                "subscription": subscription_path,
                "snapshot": snapshot_path,
            }
        )

    @staticmethod
    def is_message_exist(subscriber_client, project, subscription, expected_message_data, max_messages=100):
        messages = PubSubHelper.sync_pull(subscriber_client, project=project,
                                          subscription=subscription, max_messages=max_messages, is_ack=False)
        for message in messages:
            if message.data == expected_message_data:
                return True

        return False
