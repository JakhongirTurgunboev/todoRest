
from rest_framework import viewsets
from .serializers import TaskSerializer
from .models import Task
from .permissions import IsAuthorOrReadOnly
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = Task.objects.all()
        #queryset = Task.objects.filter(user=request.user.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer["user"] = user
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@api_view(['GET'])
def view_cached_tasks(request):
    if 'task' in cache:
        # get results from cache
        tasks = cache.get('task')
        return Response(tasks, status=status.HTTP_201_CREATED)
    else:
        tasks = Task.objects.all()
        results = [task.to_json() for task in tasks]
        # store data in cache
        cache.set("task", results, timeout=CACHE_TTL)
        return Response(results, status=status.HTTP_201_CREATED)