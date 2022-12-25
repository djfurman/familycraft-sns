from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import event_source, SNSEvent
from aws_lambda_powertools.utilities.typing import LambdaContext

log = Logger(log_uncaught_exceptions=True, use_rfc3339=True, utc=True)


@event_source(data_class=SNSEvent)
@log.inject_lambda_context(log_event=True)
def lambda_handler(event: SNSEvent, context: LambdaContext) -> None:
    log.info("Handler Invoked")

    for idx, record in enumerate(event.records):
        log.info("Invoked record processing %s times" % idx)
        log.info(record.raw_event)

    return True
