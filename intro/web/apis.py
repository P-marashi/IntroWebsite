from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from intro.projects import models
from intro.projects import serializers as ProjectsSerializers


# Create your views here.
class IndexAPIView(APIView):
    def get(self, request):
        projects = models.Projects.objects.order_by('-id')
        serializer = ProjectsSerializers.ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
