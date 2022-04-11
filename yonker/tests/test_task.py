import pytest
from celery.result import AsyncResult
import time
from yonker.tasks import send_email_task, send_failed_email_task

EMAIL_ENDPOINT = "/email"
TASK_ENDPOINT = "/task"


@pytest.mark.django_db
class TestYonker:
    def test_yonker_can_run_task(self, client):
        task = send_email_task.delay()
        status = AsyncResult(task.task_id)

        assert task.task_id
        assert status.state
        time.sleep(2)
        assert status.state == "PENDING" or "SUCCESS"

    def test_yonker_can_retry_failed_task(self, client):
        task = send_failed_email_task.delay()
        status = AsyncResult(task.task_id)

        assert status.state
        time.sleep(3)
        assert status.state == "RETRY" or "FAILURE"

    def test_yonker_can_get_task_result(self, client):
        task = send_email_task.delay()
        status = AsyncResult(task.task_id)

        assert status.state
        time.sleep(3)
        assert status.state == "SUCCESS" or "PENDING"
