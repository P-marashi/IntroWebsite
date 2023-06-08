from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from drf_spectacular.utils import extend_schema
from intro.core.serializers import EmptySerializer

from intro.projects.models import Projects
from intro.blog.models import BlogPost
from intro.chat.models import Chat
from intro.support.models import Ticket
from intro.utils.randoms import RandomGenerator
from intro.utils.renderer import UserRenderer

from .serializers import StatsSerializer


# Create your views here.
@extend_schema(tags=["web End-point"])
class IndexAPIView(APIView):
    """ Intro project root API """
    renderer_classes = [UserRenderer]
    permission_classes = (AllowAny,)

    @extend_schema(request=EmptySerializer, responses={200: StatsSerializer})
    def get(self, request):
        """ Accept get request for retrieving
            Projects, Posts, Tickets, Users datas
        """
        request.session["anonymous_user_id"] = RandomGenerator(
            encode_to_base64=1).generate_unique_hash()
        last_tickets = Ticket.objects.order_by('-id')[:5]
        last_posts = BlogPost.objects.order_by('-id')[:5]
        last_projects = Projects.objects.order_by('-id')[:5]
        stats = {
            'blog': None,
            'tickets': last_tickets,
            'posts': last_posts,
            'projects': last_projects,
        }
        serializer = StatsSerializer(stats, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["web End-point"])
class DashboardAPIView(APIView):
    """ An APIView for users dashboards """
    renderer_classes = [UserRenderer]
    permission_classes = (IsAuthenticated,)

    def get_serializer(self):
        if self.request.is_superuser:
            tickets = Ticket.objects.order_by('-id')
            posts = BlogPost.objects.order_by('-id')
            chats = Chat.objects.order_by('-id')
            projects = Projects.objects.order_by('-id')
            users = get_user_model().objects.order_by('-id')
            stats = {
                'tickets': tickets,
                'posts': posts,
                'chats': chats,
                'projects': projects,
                'users': users
            }
        else:
            tickets = Ticket.objects.filter(user=self.request.user)
            posts = BlogPost.objects.filter(user=self.request.user)
            chats = Chat.objects.filter(
                Q(sender=self.request.user) |
                Q(anonymous_sender=self.request['anonymous_user_id']))
            projects = Projects.objects.filter(user=self.request.user)
            user = self.request.user
            stats = {
                'tickets': tickets,
                'posts': posts,
                'chats': chats,
                'projects': projects,
                'users': user
            }
        return StatsSerializer(stats)

    @extend_schema(request=EmptySerializer, responses={200: StatsSerializer})
    def get(self, request):
        serializer = self.get_serializer()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
