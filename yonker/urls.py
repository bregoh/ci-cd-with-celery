from django.urls import path

from yonker.views import SendEmailView, GetTaskInfoView, SendFailedEmailView

urlpatterns = [
    path("email", SendEmailView.as_view(), name="c-email"),
    path("failed", SendFailedEmailView.as_view(), name="failed-task"),
    path("task/<str:task_id>", GetTaskInfoView.as_view(), name="c-task"),
]
