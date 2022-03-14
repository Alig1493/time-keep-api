from django.contrib.auth import get_user_model
from django.db import models

from time_keep_api.base.models import TimeStampedModel

User = get_user_model()


class Schedule(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="start_datetime_greater_than_end_datetime",
                check=models.Q(start_datetime__lt=models.F("end_datetime")),
            ),
            models.UniqueConstraint(
                name="user_start_datetime",
                fields=["user", "start_datetime"]
            ),
            models.UniqueConstraint(
                name="user_end_datetime",
                fields=["user", "end_datetime"],
                condition=models.Q(end_datetime__isnull=False)
            )
        ]

    def __str__(self):
        return f"{self.id}-{self.user}-{self.start_datetime}-{self.end_datetime}"
