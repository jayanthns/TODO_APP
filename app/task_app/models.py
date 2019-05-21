from django.db import models

# Create your models here.


class Task(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=20, default="pending")
    deleted = models.BooleanField(default=False)  # True - Deleted record.

    def __str__(self):
        return self.title

    class Meta:
        db_table = "tasks"
