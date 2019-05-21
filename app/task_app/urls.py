from django.urls import path

from app.task_app.views import todo_view, todo_details


urlpatterns = [
    path('', view=todo_view),
    path('<int:pk>/', view=todo_details),
]
