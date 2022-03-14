from random import randint

from django.urls import reverse
from django.utils import timezone

from time_keep_api.schedules.models import Schedule
from time_keep_api.schedules.tests.factories import ScheduleFactory


class TestSchedulesList:
    url = reverse("api_v1:schedules:list")

    def test_list_user_schedules(self, user, auth_client):
        start_datetime = timezone.now()
        size = randint(3, 6)
        for index in range(size):
            end_datetime = start_datetime + timezone.timedelta(minutes=5)
            ScheduleFactory(
                user=user, start_datetime=start_datetime, end_datetime=end_datetime
            )
            start_datetime = end_datetime
        response = auth_client.get(self.url)
        assert response.status_code == 200
        assert response.json().get("count") == size


class TestScheduleClockIn:
    url = reverse("api_v1:schedules:clock-in")

    def test_clock_in(self, user, auth_client):
        response = auth_client.post(self.url)
        assert response.status_code == 200
        assert Schedule.objects.filter(
            user=user,
            start_datetime__date=timezone.now().date(),
            end_datetime__isnull=True
        ).count() == 1

    def test_clock_in_without_having_previously_clocked_out(self, user, auth_client):
        schedule = ScheduleFactory(user=user, start_datetime=timezone.now())
        assert Schedule.objects.filter(
            user=user,
            start_datetime=schedule.start_datetime,
            end_datetime__isnull=True
        ).count() == 1
        response = auth_client.post(self.url)
        assert response.status_code == 400
        assert response.json() == ["Has unclocked entries for {}".format(user.username)]
        assert Schedule.objects.filter(
            user=user,
            start_datetime=schedule.start_datetime,
            end_datetime__isnull=True
        ).count() == 1


class TestScheduleClockOut:
    url = reverse("api_v1:schedules:clock-out")

    def test_clock_out(self, user, auth_client):
        clock_in_schedule = ScheduleFactory(user=user, start_datetime=timezone.now())
        response = auth_client.post(self.url)
        assert response.status_code == 200
        assert Schedule.objects.filter(
            user=user,
            start_datetime=clock_in_schedule.start_datetime,
            end_datetime__isnull=False
        ).count() == 1

    def test_clock_out_without_having_previously_clocked_in(self, user, auth_client):
        response = auth_client.post(self.url)
        assert response.status_code == 400
        assert response.json() == ["Has no prior clock in times to clock out from for {}".format(user.username)]
