import pytest
from django.db import IntegrityError
from django.utils import timezone

from time_keep_api.schedules.tests.factories import ScheduleFactory
from time_keep_api.users.tests.factories import UserFactory


class TestScheduleConstraint:

    def test_end_greater_than_start(self):
        with pytest.raises(IntegrityError) as constrain_error:
            ScheduleFactory(
                start_datetime=timezone.now(), end_datetime=timezone.now() - timezone.timedelta(minutes=1)
            )
        assert "start_datetime_greater_than_end_datetime" in constrain_error.value.args[0]

    def test_unique_user_start_datetime(self):
        start_datetime = timezone.now()
        user = UserFactory()
        ScheduleFactory(user=user, start_datetime=start_datetime)
        with pytest.raises(IntegrityError) as constrain_error:
            ScheduleFactory(user=user, start_datetime=start_datetime)
        assert "user_start_datetime" in constrain_error.value.args[0]

    def test_unique_user_end_datetime(self):
        start_datetime = timezone.now()
        new_start_datetime = start_datetime + timezone.timedelta(minutes=5)
        end_datetime = new_start_datetime + timezone.timedelta(minutes=5)
        user = UserFactory()
        ScheduleFactory(user=user, start_datetime=start_datetime, end_datetime=end_datetime)
        with pytest.raises(IntegrityError) as constrain_error:
            ScheduleFactory(user=user, start_datetime=new_start_datetime, end_datetime=end_datetime)
        assert "user_end_datetime" in constrain_error.value.args[0]
