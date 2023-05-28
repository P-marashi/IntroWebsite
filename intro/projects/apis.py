from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from intro.core.serializers import EmptySerializer

from . import serializers
from . import models


class CreateProjectAPIView(APIView):
    @extend_schema(request=serializers.ProjectSerializer, responses={
        201: serializers.ProjectSerializer
    })
    def post(self, request):
        serializer = serializers.ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(serializers.ProjectSerializer(instance),
                        status=status.HTTP_201_CREATED)


class CreateProjectFeatureAPIView(APIView):
    @extend_schema(request=serializers.FeatureSerializer, responses={
        201: serializers.ProjectSerializer
    })
    def post(self, request, project_pk):
        project = get_object_or_404(models.Projects, pk=project_pk)
        serializer = serializers.FeatureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        project.features.add(instance)
        project.features.save()
        return Response(serializers.ProjectSerializer(instance),
                        status=status.HTTP_201_CREATED)


class UpdateProjectFeatureAPIView(APIView):
    @extend_schema(request=serializers.FeatureSerializer, responses={
        200: serializers.ProjectSerializer
    })
    def put(self, request, project_pk, feature_pk):
        project = get_object_or_404(models.Projects, pk=project_pk)
        feature = get_object_or_404(models.Features, pk=feature_pk)
        serializer = serializers.FeatureSerializer(feature, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializers.ProjectSerializer(project),
                        status=status.HTTP_200_OK)


class DestroyProjectFeatureAPIView(APIView):
    @extend_schema(request=EmptySerializer, responses={204: EmptySerializer})
    def delete(self, request, project_pk, feature_pk):
        project = get_object_or_404(models.Projects, pk=project_pk)
        feature = get_object_or_404(models.Features, pk=feature_pk)
        project.features.delete(feature)
        project.features.save()
        return Response(EmptySerializer, status=status.HTTP_204_NO_CONTENT)


class ListProjectFeatureAPIView(APIView):
    @extend_schema(request=EmptySerializer, responses={
        200: serializers.FeatureSerializer
    })
    def get(self, request, project_pk):
        project = get_object_or_404(models.Projects, pk=project_pk)
        serializer = serializers.FeatureSerializer(project.features)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateProjectImageExampleAPIView(APIView):
    @extend_schema(request=serializers.ImageSerializer, responses={
        201: serializers.ProjectSerializer
    })
    def post(self, request, project_pk):
        project = get_object_or_404(models.Projects, pk=project_pk)
        serializer = serializers.ImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        project.images.add(instance)
        project.images.save()
        return Response(serializers.ProjectSerializer(project),
                        status=status.HTTP_201_CREATED)


class UpdateProjectImageExampleAPIView(APIView):
    @extend_schema(request=serializers.ImageSerializer, responses={
        200: serializers.ProjectSerializer
    })
    def put(self, request, project_pk, image_pk):
        project = get_object_or_404(models.Projects, pk=project_pk)
        image = get_object_or_404(models.ImageExamples, pk=image_pk)
        serializer = serializers.ImageSerializer(instance=image,
                                                 data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializers.ProjectSerializer(project),
                        status=status.HTTP_200_OK)


class ListProjectImageExampleAPIView(APIView):
    @extend_schema(request=EmptySerializer, responses={
        200: serializers.ImageSerializer
    })
    def get(self, request, project_pk):
        project = get_object_or_404(models.Projects, pk=project_pk)
        serializer = serializers.ImageSerializer(project.images)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DestroyProjectImageExampleAPIView(APIView):
    @extend_schema(request=EmptySerializer, responses={204: EmptySerializer})
    def delete(self, request, project_pk, image_pk):
        project = get_object_or_404(models.Projects, pk=project_pk)
        image = get_object_or_404(models.ImageExamples, pk=image_pk)
        project.images.delete(image)
        project.images.save()
        return Response(EmptySerializer, status=status.HTTP_204_NO_CONTENT)


class UpdateProjectAPIView(APIView):
    @extend_schema(request=serializers.ProjectSerializer, responses={
        200: serializers.ProjectSerializer
    })
    def put(self, request, project_pk):
        project = get_object_or_404(models.Projects, pk=project_pk)
        serializer = serializers.ProjectSerializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(serializers.ProjectSerializer(instance),
                        status=status.HTTP_200_OK)


class RetrieveProjectAPIView(APIView):
    @extend_schema(request=serializers.ProjectSerializer, responses={
        200: serializers.ProjectSerializer
    })
    def get(self, request, project_pk):
        project = get_object_or_404(models.Projects, pk=project_pk)
        serializer = serializers.ProjectSerializer(project)
        return Response(serializer, status=status.HTTP_200_OK)


class ListProjectAPIView(APIView):
    @extend_schema(request=EmptySerializer, responses={
        200: serializers.ProjectSerializer
    })
    def get(self, request):
        projects = models.Projects.objects.order_by('-id')
        serializer = serializers.ProjectSerializer(projects)
        return Response(serializer, status=status.HTTP_200_OK)


class DestroyProjectAPIView(APIView):
    @extend_schema(request=EmptySerializer, responses={204: EmptySerializer})
    def delete(self, request, project_pk):
        project = get_object_or_404(models.Projects, pk=project_pk)
        project.delete()
        return Response(EmptySerializer, status=status.HTTP_204_NO_CONTENT)
