from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CustomUser
from rest_framework import viewsets, status
from rest_framework import permissions
from .serializers import CustomUserSerializer
from django.contrib.auth.hashers import make_password

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from todo.models import Task
from todo.serializers import TaskSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
@api_view(['GET'])
def hello_world(request):
    if 'task' in cache:
        # get results from cache
        tasks = cache.get('task')
        return Response(tasks, status=status.HTTP_201_CREATED)
    else:
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        results = serializer.data
        # store data in cache
        cache.set("task", results, timeout=CACHE_TTL)
        return Response(results, status=status.HTTP_201_CREATED)