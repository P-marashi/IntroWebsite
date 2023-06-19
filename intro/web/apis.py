from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

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

    # @method_decorator(cache_page(60*60*3))
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
        stats = StatsSerializer({
            'blog': last_posts,
            'chat': None,
            'project': last_projects,
            'ticket': last_tickets,
        })
        return Response(data=stats.data, status=status.HTTP_200_OK)


@extend_schema(tags=["web End-point"])
class DashboardAPIView(APIView):
    """ An APIView for users dashboards """
    renderer_classes = [UserRenderer]
    permission_classes = (IsAuthenticated,)

    def get_stats(self, blog: object = None, chat: object = None,
                  project: object = None, ticket: object = None, user: object = None):
        stats = StatsSerializer({
            'blog': blog,
            'chat': chat,
            'project': project,
            'ticket': ticket,
            'user': user
        }, context={'request': self.request})
        return stats

    # @method_decorator(cache_page(60*60*3))
    # @method_decorator(vary_on_headers("Authorization",))
    @extend_schema(request=EmptySerializer, responses={200: StatsSerializer})
    def get(self, request):
        blog = BlogPost.objects.all()
        chat = Chat.objects.all()
        project = Projects.objects.all()
        ticket = Ticket.objects.all()
        stats = self.get_stats(blog, chat, project, ticket, user=None)
        return Response(stats.data, status=status.HTTP_200_OK)
