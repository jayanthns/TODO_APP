import csv
from django.http import HttpResponse

from django.contrib import admin

from app.task_app.models import Task

# Register your models here.


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id', 'title', 'description', 'scheduled_at',
                    'created_at', 'modified_at', 'deleted', 'status')
    list_filter = ('id', 'title', 'scheduled_at', 'deleted', 'status')
    search_fields = ['title']
    actions = ["export_as_csv"]
