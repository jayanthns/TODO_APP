from django.http import HttpResponse
from django.shortcuts import render, redirect

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app.task_app.models import Task
from app.task_app.serializers import (
    TaskCreateSerializer,
    TaskSerializer,
    TaskSwaggerSerializer,
    TaskListSwaggerSerializer,
    MessageResponseSerializer
)


# Swagger responses
task_detail_response = openapi.Response('Task response', TaskSwaggerSerializer)
task_list_response = openapi.Response('Task List', TaskListSwaggerSerializer)
message_response = openapi.Response('response_description', MessageResponseSerializer)


def task_form(request):
    if request.method == "GET":
        return render(request, 'task_form.html')


# def task_details(request, pk):
#     if request.method == "GET":
#         return render(request, 'task_form.html')


def task_list(request):
    if request.method == "GET":
        task_queryset = Task.objects.filter(deleted=False)
        return render(request, 'task_list.html', {"data": task_queryset})


@swagger_auto_schema(methods=['get'],
                     responses={200: task_list_response},
                     tags=['Task List API'])
@swagger_auto_schema(methods=['post'],
                     request_body=TaskCreateSerializer,
                     responses={201: message_response},
                     tags=["Task Create API"])
@api_view(['GET', 'POST'])
def todo_view(request):
    if request.method == 'GET':
        serializer = TaskSerializer(Task.objects.filter(deleted=False), many=True)
        return Response(
            {
                "data": serializer.data,
                "message": "Data fetched successfully.",
                "status": status.HTTP_200_OK
            },
            status=status.HTTP_200_OK
        )
    if request.method == 'POST':
        serializer = TaskCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "data": serializer.errors,
                    "message": "incorrect data were provided.",
                    "status": status.HTTP_400_BAD_REQUEST
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {
                "message": "Task created successfully.",
                "status": status.HTTP_201_CREATED
            },
            status=status.HTTP_201_CREATED
        )


@swagger_auto_schema(methods=['get'],
                     responses={200: task_detail_response},
                     tags=['Task Detail API'])
@swagger_auto_schema(methods=['put'],
                     request_body=TaskCreateSerializer,
                     responses={200: message_response},
                     tags=["Task update API"])
@swagger_auto_schema(methods=['delete'],
                     responses={200: message_response},
                     tags=["Task Delete API"])
@api_view(['GET', 'PUT', 'DELETE'])
def todo_details(request, pk):
    try:
        task_obj = Task.objects.get(id=pk, deleted=False)
    except:
        return Response(
            {
                "message": "task not found",
                "status": status.HTTP_404_NOT_FOUND
            },
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = TaskSerializer(task_obj)
        return Response(
            {
                "data": serializer.data,
                "message": "Data fetched successfully.",
                "status": status.HTTP_200_OK
            },
            status=status.HTTP_200_OK
        )
    if request.method == 'PUT':
        serializer = TaskCreateSerializer(task_obj, data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "data": serializer.errors,
                    "message": "incorrect data were provided.",
                    "status": status.HTTP_400_BAD_REQUEST
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {
                "message": "Task updated successfully.",
                "status": status.HTTP_200_OK
            },
            status=status.HTTP_200_OK
        )
    if request.method == "DELETE":
        task_obj.deleted = True
        task_obj.save()
        return Response(
            {
                "message": "Task deleted successfully.",
                "status": status.HTTP_200_OK
            },
            status=status.HTTP_200_OK
        )
