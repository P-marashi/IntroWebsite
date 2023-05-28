from rest_framework import serializers

from intro.blog.serializers import BlogPostSerializer
from intro.chat.serializers import ChatSerializer
from intro.projects.serializers import ProjectSerializer
from intro.support.serializers import TicketSerializer
from intro.users.serializers import UserSerializer


class StatsSerializer(serializers.Serializer):
    """ Stats Serializer for user dashboard """

    blog = BlogPostSerializer(many=True, required=False)
    chat = ChatSerializer(many=True, required=False)
    project = ProjectSerializer(many=True, required=False)
    ticket = TicketSerializer(many=True, required=False)
    user = UserSerializer(many=True, required=False)
