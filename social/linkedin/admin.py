from django.contrib import admin

from . import models
from reusable.admins import ReadOnlyAdminDateFields


@admin.register(models.JobPage)
class JobPageAdmin(ReadOnlyAdminDateFields, admin.ModelAdmin):
    list_display = ("pk", "name", "enable", "last_crawl_at")
