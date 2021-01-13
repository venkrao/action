import logging
import boto3
import os
from actio import settings

logger = logging.getLogger(__name__)
logging.disable(logging.NOTSET)
logger.setLevel(logging.DEBUG)


class Boto3Wrapper():
    def __init__(self):
        client = boto3.client(
            "sns",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        self.client = client

    def sns_create_topic(self, client=None, topic_name=None):
        topic = client.create_topic(Name=topic_name)
        return topic

    def sns_create_subscription(self, topic_arn=None, protocol=None, endpoint=None):
        self.client.subscribe(
            TopicArn=topic_arn,
            Protocol=protocol,
            Endpoint=endpoint
        )

    def sns_publish(self, message=None, target_arn=None):
        self.client.publish(Message=message, TargetArn=target_arn)


if __name__ == "__main__":
    boto = Boto3Wrapper()
    boto.sns_publish(message="Hello push notification", target_arn="arn:aws:sns:eu-central-1:435865654340:endpoint/BAIDU/actio-app/08e80483-19ef-34c5-a733-0d3c92415077")
