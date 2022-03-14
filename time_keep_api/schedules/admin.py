from django.contrib import admin

# Register your models here.
from time_keep_api.schedules.models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "start_datetime", "end_datetime"]
