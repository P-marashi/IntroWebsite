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
    permission_classes = (IsAdminOrSelfOrReadOnly, )
    model = models.Projects
    serializer_class = serializers.ProjectSerializer

    @extend_schema(request=serializer_class, responses={
        201: serializer_class})
    def post(self, request):
        """ Create a Project """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(user=request.user)
        return Response(self.serializer_class(instance).data,
                        status=status.HTTP_201_CREATED)

    @extend_schema(request=EmptySerializer, responses={
        200: serializer_class})
    def get(self, request):
        """ List all Projects by reverse ordering """
        projects = self.model.objects.order_by('-id')
        serializer = self.serializer_class(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Projects End-point"])
class RetrieveUpdateDestroyProjectAPIView(APIView):
    """ An APIView for retrieving, updating, destroying projects """

    renderer_classes = [UserRenderer]
    permission_classes = (IsAdminOrSelfOrReadOnly, )
    model = models.Projects
    serializer_class = serializers.ProjectSerializer

    @extend_schema(request=serializer_class, responses={
        200: serializer_class})
    def get(self, request, slug):
        """ Retrieve project information by primary key """
        project = get_object_or_404(self.model, slug=slug)
        serializer = self.serializer_class(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=serializer_class, responses={
        200: serializer_class})
    def put(self, request, slug):
        """ Update project information by primary key """
        project = get_object_or_404(self.model, slug=slug)
        serializer = self.serializer_class(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(self.serializer_class(instance).data,
                        status=status.HTTP_200_OK)

    @extend_schema(request=EmptySerializer, responses={204: EmptySerializer})
    def delete(self, request, slug):
        """ Destroy project object by primary key """
        project = get_object_or_404(self.model, slug=slug)
        project.delete()
        return Response(EmptySerializer().data, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Projects End-point"])
class ListCreateProjectFeatureAPIView(APIView):
    """ An APIView for Listing and Creating Project Features """

    renderer_classes = [UserRenderer]
    permission_classes = (IsAdminOrSelfOrReadOnly, )
    model = models.Projects
    serializer_classes = {
        'feature': serializers.FeatureSerializer,
        'project': serializers.ProjectSerializer
    }

    @extend_schema(request=serializer_classes['feature'], responses={
        201: serializer_classes['project']})
    def post(self, request, slug):
        """ Create Project Feature """
        project = self.model.objects.prefetch_related('features').get(slug=slug)
        serializer = self.serializer_classes['feature'](data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        project.features.add(instance)
        return Response(self.serializer_classes['project'](project).data,
                        status=status.HTTP_201_CREATED)

    @extend_schema(request=EmptySerializer, responses={
        200: serializer_classes['feature']})
    def get(self, request, slug):
        """ List project features """
        project = self.model.objects.prefetch_related('features').get(slug=slug)
        serializer = self.serializer_classes['feature'](project.features, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Projects End-point"])
class UpdateDestroyProjectFeatureAPIView(APIView):
    """ An APIView for updating, destroying project feature """

    renderer_classes = [UserRenderer]
    permission_classes = (IsAdminOrSelfOrReadOnly, )
    model = models.Projects
    serializer_classes = {
        'feature': serializers.FeatureSerializer,
        'project': serializers.ProjectSerializer
    }

    @extend_schema(request=serializer_classes['feature'], responses={
        200: serializer_classes['project']})
    def put(self, request, slug, feature_pk):
        """ Update project features """
        project = self.model.objects.prefetch_related('features').get(slug=slug)
        feature = project.features.get(pk=feature_pk)
        serializer = self.serializer_classes['feature'](feature, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(self.serializer_classes['project'](project).data,
                        status=status.HTTP_200_OK)

    @extend_schema(request=EmptySerializer, responses={204: EmptySerializer})
    def delete(self, request, slug, feature_pk):
        """ Destroy project feature """
        project = self.model.objects.prefetch_related('features').get(slug=slug)
        feature = project.features.get(pk=feature_pk)
        project.features.remove(feature)
        return Response(EmptySerializer().data, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Projects End-point"])
class ListCreateProjectImageExampleAPIView(APIView):
    """ An APIView for Creating and listing Project Images """

    renderer_classes = [UserRenderer]
    permission_classes = (IsAdminOrSelfOrReadOnly, )
    model = models.Projects
    serializer_classes = {
        'image': serializers.ImageSerializer,
        'project': serializers.ProjectSerializer,
    }

    @extend_schema(request=serializer_classes['image'], responses={
        201: serializer_classes['project']})
    def post(self, request, slug):
        """ Create project image """
        project = self.model.objects.prefetch_related('images').get(slug=slug)
        serializer = self.serializer_classes['image'](data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        project.images.add(instance)
        return Response(self.serializer_classes['project'](project).data,
                        status=status.HTTP_201_CREATED)

    @extend_schema(request=EmptySerializer, responses={
        200: serializer_classes['image']})
    def get(self, request, slug):
        """ List project images """
        project = self.model.objects.prefetch_related('images').get(slug=slug)
        serializer = self.serializer_classes['image'](project.images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Projects End-point"])
class UpdateDestroyProjectImageExampleAPIView(APIView):
    """ An APIView for Updating, destroying project image """

    renderer_classes = [UserRenderer]
    permission_classes = (IsAdminOrSelfOrReadOnly, )
    model = models.Projects
    serializer_classes = {
        'image': serializers.ImageSerializer,
        'project': serializers.ProjectSerializer,
    }

    @extend_schema(request=serializer_classes['image'], responses={
        200: serializer_classes['project']})
    def put(self, request, slug, image_pk):
        """ Update project image """
        project = self.model.objects.prefetch_related('images').get(slug=slug)
        image = project.images.get(pk=image_pk)
        serializer = self.serializer_classes['image'](instance=image,
                                                      data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(self.serializer_classes['project'](project).data,
                        status=status.HTTP_200_OK)

    @extend_schema(request=EmptySerializer, responses={204: EmptySerializer})
    def delete(self, request, slug, image_pk):
        """ Destroy project image """
        project = self.model.objects.prefetch_related('images').get(slug=slug)
        image = project.images.get(pk=image_pk)
        project.images.remove(image)
        return Response(EmptySerializer().data, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Projects End-point"])
class ListCreateCommentAPIView(APIView):
    """ An APIView for list and creating Comment objects """

    renderer_classes = [UserRenderer]
    permission_classes = (IsAdminOrSelfOrReadOnly, )
    model = models.Projects
    serializer_classes = {
        'comment': serializers.CommentSerializer,
        'project': serializers.ProjectSerializer,
    }

    @extend_schema(request=EmptySerializer, responses={
        200: serializers.CommentSerializer})
    def get(self, request, slug):
        """ Retrieve list of comment objects """
        project = self.model.objects.prefetch_related('comments').get(slug=slug)
        serializer = self.serializer_classes['comment'](project.comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=serializers.CommentSerializer, responses={
        201: serializers.CommentSerializer})
    def post(self, request, slug):
        """ Create a new object of Comment """
        project = self.model.objects.prefetch_related('comments').get(slug=slug)
        serializer = self.serializer_classes['comment'](data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, project=project)
        return Response(self.serializer_classes['project'](project).data,
                        status=status.HTTP_201_CREATED)


@extend_schema(tags=["Projects End-point"])
class UpdateDestroyCommentAPIView(APIView):
    """ An APIView for update and destroy Comments """

    renderer_classes = [UserRenderer]
    permission_classes = (IsAdminOrSelfOrReadOnly, )
    model = models.Projects
    serializer_classes = {
        'comment': serializers.CommentSerializer,
        'project': serializers.ProjectSerializer,
    }

    @extend_schema(request=serializer_classes['comment'], responses={
        200: serializer_classes['project']})
    def put(self, request, slug, comment_pk):
        """ An APIView for update comment """
        project = self.model.objects.prefetch_related('comments').get(slug=slug)
        comment = project.comments.get(pk=comment_pk)
        serializer = self.serializer_classes['comment'](comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            self.serializer_classes['project'](project).data,
            status=status.HTTP_200_OK)

    @extend_schema(request=EmptySerializer, responses={204: EmptySerializer})
    def delete(self, request, slug, comment_pk):
        """ An APIView for delete comment """
        project = self.model.objects.prefetch_related('comments').get(slug=slug)
        comment = project.comments.get(pk=comment_pk)
        comment.delete()
        return Response(EmptySerializer().data, status=status.HTTP_204_NO_CONTENT)
