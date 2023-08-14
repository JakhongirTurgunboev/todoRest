from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from . import views

from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()

router.register(r'todo', views.TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('/todo/cache', views.view_cached_tasks)
]