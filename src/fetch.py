import logging

from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def getRetryWrapper(RETRYABLE_ERRORS):
    return retry(
        stop=stop_after_attempt(20),
        wait=wait_random_exponential(multiplier=4, min=4, max=600),
        retry=retry_if_exception_type(RETRYABLE_ERRORS),
        # before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )


def safeFetch(function, RETRYABLE_ERRORS, *args, **kwargs):
    wrapper = getRetryWrapper(RETRYABLE_ERRORS)
    return wrapper(function)(*args, **kwargs)
