from rest_framework import serializers

from time_keep_api.schedules.models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ["id", "user", "start_datetime", "end_datetime"]
