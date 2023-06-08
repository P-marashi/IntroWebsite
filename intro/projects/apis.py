from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from intro.core.serializers import EmptySerializer
from intro.core.permissions import IsAdminOrSelfOrReadOnly
from intro.utils.renderer import UserRenderer

from . import serializers
from . import models


@extend_schema(tags=["Projects End-point"])
class ListCreateProjectAPIView(APIView):
    """
    an APIView for List and Creating Projects Model
    """
    renderer_classes = [UserRenderer]
    permission_classes = (IsAdminOrSelfOrReadOnly,)

    @extend_schema(request=serializers.ProjectSerializer, responses={
        201: serializers.ProjectSerializer
    })
    def post(self, request):
        """ Create a Project """
        serializer = serializers.ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(commit=False)
        instance.user = request.user
        instance.save()
        return Response(serializers.ProjectSerializer(instance).data,
                        status=status.HTTP_201_CREATED)

    @extend_schema(request=EmptySerializer, responses={
        200: serializers.ProjectSerializer
    })
    def get(self, request):
        """ List all Projects by reverse ordering """
        projects = models.Projects.objects.order_by('-id')
        serializer = serializers.ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Projects End-point"])
class RetrieveUpdateDestroyProjectAPIView(APIView):
    """ An APIView for retrieving, updating, destroying projects """

    renderer_classes = [UserRenderer]
    permission_classes = (IsAdminOrSelfOrReadOnly,)

    @extend_schema(request=serializers.ProjectSerializer, responses={
        200: serializers.ProjectSerializer
    })
    def get(self, request, project_pk):
        """ Retrieve project information by primary key """
        project = get_object_or_404(models.Projects, pk=project_pk)
        serializer = serializers.ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=serializers.ProjectSerializer, responses={
        200: serializers.ProjectSerializer
    })
    def put(self, request, project_pk):
        """ Update project information by primary key """
        project = get_object_or_404(models.Projects, pk=project_pk)
        serializer = serializers.ProjectSerializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(serializers.ProjectSerializer(instance).data,
                        status=status.HTTP_200_OK)

    @extend_schema(request=EmptySerializer, responses={204: EmptySerializer})
    def delete(self, request, project_pk):
        """ Destroy project object by primary key """
        project = get_object_or_404(models.Projects, pk=project_pk)
        project.delete()
        return Response(EmptySerializer().data, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Projects End-point"])
class ListCreateProjectFeatureAPIView(APIView):
    """ An APIView for Listing and Creating Project Features """
    renderer_classes = [UserRenderer]

    permission_classes = (IsAdminOrSelfOrReadOnly,)

    @extend_schema(request=serializers.FeatureSerializer, responses={
        201: serializers.ProjectSerializer
    })
    def post(self, request, project_pk):
        """ Create Project Feature """
        project = get_object_or_404(models.Projects, pk=project_pk)
        serializer = serializers.FeatureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        project.features.add(instance)
        project.features.save()
        return Response(serializers.ProjectSerializer(instance).data,
                        status=status.HTTP_201_CREATED)

    @extend_schema(request=EmptySerializer, responses={
        200: serializers.FeatureSerializer
    })
    def get(self, request, project_pk):
        """ List project features """
        project = get_object_or_404(models.Projects, pk=project_pk)
        serializer = serializers.FeatureSerializer(project.features, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Projects End-point"])
class UpdateDestroyProjectFeatureAPIView(APIView):
    """ An APIView for updating, destroying project feature """
    renderer_classes = [UserRenderer]
    permission_classes = (IsAdminOrSelfOrReadOnly,)

    @extend_schema(request=serializers.FeatureSerializer, responses={
        200: serializers.ProjectSerializer
    })
    def put(self, request, project_pk, feature_pk):
        """ Update project features """
        project = get_object_or_404(models.Projects, pk=project_pk)
        feature = get_object_or_404(models.Features, pk=feature_pk)
        serializer = serializers.FeatureSerializer(feature, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializers.ProjectSerializer(project).data,
                        status=status.HTTP_200_OK)

    @extend_schema(request=EmptySerializer, responses={204: EmptySerializer})
    def delete(self, request, project_pk, feature_pk):
        """ Destroy project feature """
        project = get_object_or_404(models.Projects, pk=project_pk)
        feature = get_object_or_404(models.Features, pk=feature_pk)
        project.features.delete(feature)
        project.features.save()
        return Response(EmptySerializer().data, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Projects End-point"])
class ListCreateProjectImageExampleAPIView(APIView):
    """ An APIView for Creating and listing Project Images """
    renderer_classes = [UserRenderer]
    permission_classes = (IsAdminOrSelfOrReadOnly,)

    @extend_schema(request=serializers.ImageSerializer, responses={
        201: serializers.ProjectSerializer
    })
    def post(self, request, project_pk):
        """ Create project image """
        project = get_object_or_404(models.Projects, pk=project_pk)
        serializer = serializers.ImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        project.images.add(instance)
        project.images.save()
        return Response(serializers.ProjectSerializer(project).data,
                        status=status.HTTP_201_CREATED)

    @extend_schema(request=EmptySerializer, responses={
        200: serializers.ImageSerializer
    })
    def get(self, request, project_pk):
        """ List project images """
        project = get_object_or_404(models.Projects, pk=project_pk)
        serializer = serializers.ImageSerializer(project.images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Projects End-point"])
class UpdateDestroyProjectImageExampleAPIView(APIView):
    """ An APIView for Updating, destroying project image """
    renderer_classes = [UserRenderer]
    permission_classes = (IsAdminOrSelfOrReadOnly,)

    @extend_schema(request=serializers.ImageSerializer, responses={
        200: serializers.ProjectSerializer
    })
    def put(self, request, project_pk, image_pk):
        """ Update project image """
        project = get_object_or_404(models.Projects, pk=project_pk)
        image = get_object_or_404(models.ImageExamples, pk=image_pk)
        serializer = serializers.ImageSerializer(instance=image,
                                                 data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializers.ProjectSerializer(project).data,
                        status=status.HTTP_200_OK)

    @extend_schema(request=EmptySerializer, responses={204: EmptySerializer})
    def delete(self, request, project_pk, image_pk):
        """ Destroy project image """
        project = get_object_or_404(models.Projects, pk=project_pk)
        image = get_object_or_404(models.ImageExamples, pk=image_pk)
        project.images.delete(image)
        project.images.save()
        return Response(EmptySerializer().data, status=status.HTTP_204_NO_CONTENT)
