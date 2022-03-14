from django.urls import path

from time_keep_api.schedules.views import ScheduleListAPIView, ScheduleEndAPIView, ScheduleStartAPIView

app_name = "schedules"

urlpatterns = [
    path("", ScheduleListAPIView.as_view(), name="list"),
    path("clock-in/", ScheduleStartAPIView.as_view(), name="clock-in"),
    path("clock-out/", ScheduleEndAPIView.as_view(), name="clock-out"),
]
