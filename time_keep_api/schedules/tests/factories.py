from factory import DjangoModelFactory, SubFactory

from time_keep_api.schedules.models import Schedule
from time_keep_api.users.tests.factories import UserFactory


class ScheduleFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)

    class Meta:
        model = Schedule
