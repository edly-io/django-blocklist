"""Just enough of a urls.py to run the tests."""
from django.http import HttpResponse
from django.urls import path

urlpatterns = [
    path('', lambda request: HttpResponse()),
]
