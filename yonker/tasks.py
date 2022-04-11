import random
from celery import shared_task
import time


@shared_task(
    name="yonker.send_email_task",
    bind=True,
)
def send_email_task(self):
    delay_time = random.choice([5, 10])
    time.sleep(delay_time)
    return "email successfully sent..."


@shared_task(
    name="yonker.send_failed_email_task",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 2},
)
def send_failed_email_task(self):
    raise Exception("error sending email..., retrying....")
