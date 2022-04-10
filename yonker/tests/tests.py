from urllib import response
import pytest
import json
from celery.result import AsyncResult
import time
from yonker.tasks import send_email_task, send_failed_email_task

EMAIL_ENDPOINT = "/email"
TASK_ENDPOINT = "/task"


@pytest.mark.django_db
class TestYonker:
    def test_yonker_can_send_email(self, client):
        response = client().post(EMAIL_ENDPOINT, format="json")
        data = json.loads(response.content)["data"]

        assert response.status_code == 201
        assert data["task_id"]

    def test_yonker_can_send_failed_email(self, client):
        response = client().post("/failed", format="json")
        data = json.loads(response.content)["data"]

        assert response.status_code == 201

    def test_yonker_task(self, client):
        task = send_email_task.delay()

        assert task.task_id

    def test_retry_failed_yonker_task(self, client):
        task = send_failed_email_task.delay()
        status = AsyncResult(task.task_id)

        assert status.state
        time.sleep(2)
        assert status.state == "RETRY"
        time.sleep(4)
        assert status.state == "FAILED" or "SUCCESS"

    def test_yonker_can_get_task_result(self, client):
        task = send_email_task.delay()
        status = AsyncResult(task.task_id)

        assert status.state
        time.sleep(7)
        assert status.state == "SUCCESS" or "PENDING"
