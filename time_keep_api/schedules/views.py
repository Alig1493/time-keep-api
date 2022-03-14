import logging

from django.db import IntegrityError
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from time_keep_api.schedules.serializers import ScheduleSerializer

logger = logging.getLogger(__name__)


class ScheduleListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        return self.request.user.schedule_set.all()


class ScheduleStartAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return

    def get_queryset(self):
        return self.request.user.schedule_set.filter(end_datetime__isnull=True)

    def create(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.count() > 0:
            raise ValidationError(
                detail="Has unclocked entries for {}".format(self.request.user.username),
                code="unclocked_entries_error"
            )
        try:
            self.request.user.schedule_set.create(start_datetime=timezone.now())
        except IntegrityError as db_integrity_error:
            logger.error(db_integrity_error)
            raise ValidationError(
                detail="Failed to create an entry for {}".format(self.request.user.username),
                code="start_datetime_entry_create_error"
            )
        return Response(status=status.HTTP_200_OK)


class ScheduleEndAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return

    def get_queryset(self):
        return self.request.user.schedule_set.filter(
            start_datetime__lte=timezone.now(),
            end_datetime__isnull=True
        )

    def create(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.count() < 1:
            raise ValidationError(
                detail="Has no prior clock in times to clock out from for {}".format(request.user.username),
                code="no_prior_start_datetime"
            )
        try:
            schedule = queryset.latest("start_datetime")
            schedule.end_datetime = timezone.now()
            schedule.save()
        except IntegrityError as db_integrity_error:
            logger.error(db_integrity_error)
            raise ValidationError(
                detail="Failed to update an entry for {}".format(self.request.user.username),
                code="end_datetime_entry_create_error"
            )
        return Response(status=status.HTTP_200_OK)
