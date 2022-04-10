from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from yonker.tasks import send_email_task, send_failed_email_task


class SendEmailView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        try:
            task = send_email_task.delay()
            response = {"data": {"task_id": task.task_id}}
            return Response(data=response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {"data": {"task_id": task.task_id}, "error": str(e)}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class SendFailedEmailView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        try:
            task = send_failed_email_task.delay()
            response = {"data": {"task_id": task.task_id}}
            return Response(data=response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {"error": str(e)}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class GetTaskInfoView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        task_id = kwargs["task_id"]
        print(task_id)

        task = AsyncResult(task_id)
        if task.state == "FAILURE":
            response = {
                "status": task.state,
                "error": str(task.result),
            }
        elif task.state == "STARTED":
            response = {
                "status": task.state,
                "data": [],
            }
        else:
            response = {
                "status": task.state,
                "data": task.result,
            }

        return Response(data=response, status=status.HTTP_200_OK)
