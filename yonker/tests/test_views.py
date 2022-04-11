import pytest
import json
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
        assert data["task_id"]

    def test_yonker_can_get_success_task_result(self, client):
        task = send_email_task.delay()
        response = client().get(f"/task/{task.task_id}")
        data = json.loads(response.content)

        assert response.status_code == 200
        assert data["status"]
        time.sleep(7)
        assert data["status"] == "SUCCESS" or "PENDING"

    def test_yonker_can_get_failed_task_result(self, client):
        task = send_failed_email_task.delay()
        response = client().get(f"/task/{task.task_id}")
        data = json.loads(response.content)

        assert response.status_code == 200
        assert data["status"]
        time.sleep(7)
        assert data["status"] == "FAILURE" or "PENDING"
