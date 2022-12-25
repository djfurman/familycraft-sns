import os
from uuid import uuid4
import pytest
from aws_lambda_powertools.utilities.typing import LambdaContext
from family_craft import app


class MockContext:
    function_name: str = "mock_function"
    memory_limit_in_mb: int = 128

    def __init__(self, region: str = None, account_id: int = None) -> None:
        if region is not None or os.getenv("AWS_REGION") is not None:
            use_region = region
        else:
            use_region = "us-east-1"

        if account_id:
            use_account = account_id
        else:
            use_account = "123456789012"

        self.invoked_function_arn: str = (
            f"arn:aws:lambda:{use_region}:{use_account}:function/mock_function"
        )

        self.aws_request_id = str(uuid4())


@pytest.fixture()
def mock_context() -> LambdaContext:
    return MockContext()


@pytest.fixture()
def sns_event() -> dict:
    """Generates SNS Event"""

    return {
        "Records": [
            {
                "EventSource": "aws:sns",
                "EventVersion": "1.0",
                "EventSubscriptionArn": "arn:aws:sns:us-east-1::ExampleTopic",
                "Sns": {
                    "Type": "Notification",
                    "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                    "TopicArn": "arn:aws:sns:us-east-1:123456789012:ExampleTopic",
                    "Subject": "example subject",
                    "Message": "example message",
                    "Timestamp": "1970-01-01T00:00:00.000Z",
                    "SignatureVersion": "1",
                    "Signature": "EXAMPLE",
                    "SigningCertUrl": "EXAMPLE",
                    "UnsubscribeUrl": "EXAMPLE",
                    "MessageAttributes": {
                        "Test": {"Type": "String", "Value": "TestString"},
                        "TestBinary": {"Type": "Binary", "Value": "TestBinary"},
                    },
                },
            }
        ]
    }


def test_lambda_handler(sns_event: dict, mock_context: LambdaContext) -> None:

    res = app.lambda_handler(sns_event, mock_context)
    print(res)
    assert res
    # data = json.loads(ret["body"])
