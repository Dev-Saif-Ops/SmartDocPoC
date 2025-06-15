from django.urls import path
from django.http import JsonResponse


def say_hello(request):
    """Returns a friendly hello"""
    return JsonResponse({"msg": "Hello from Django"})


urlpatterns = [
    path("hello/", say_hello)
]
