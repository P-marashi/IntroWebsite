from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import AuthenticationFailed

from drf_spectacular.utils import extend_schema

from intro.core.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, IsAdminOrAuthenticatedUser
from intro.core.serializers import EmptySerializer
from intro.utils.renderer import UserRenderer

from .models import Ticket
from .serializers import TicketSerializer


@extend_schema(tags=["Supports End-point"])
class TicketListCreateView(APIView):
    permission_classes = [IsAdminOrAuthenticatedUser]

    @extend_schema(request=TicketSerializer, responses={200: TicketSerializer})
    def get(self, request):
        """
        Retrieve a list of tickets based on the user's authentication and admin status.
        Only authenticated users can access the tickets.
        Admin users can access all tickets, while regular users can only access their own tickets.
        """
        if not request.user.is_authenticated:
            raise AuthenticationFailed()

        if request.user.is_admin:
            tickets = Ticket.objects.all()
        else:
            tickets = Ticket.objects.filter(user=request.user)

        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new ticket.
        """
        serializer = TicketSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketDetailView(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_ticket(self, pk):
        """
        Retrieve a ticket instance based on the provided ID (pk).
        The ticket can only be retrieved if the user is the owner or a superuser.
        """
        try:
            ticket = Ticket.objects.get(id=pk)
            if self.request.user.is_superuser or ticket.user == self.request.user:
                return ticket
            else:
                return None
        except Ticket.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve a ticket based on the provided ID (pk).
        """
        ticket = self.get_ticket(pk)
        if ticket:
            serializer = TicketSerializer(ticket)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        ticket = self.get_ticket(pk)
        if ticket:
            if ticket.user == request.user:  # Only allow users to edit their own tickets
                if ticket.status == 'closed' and not request.user.is_admin:
                    return Response({'message': 'Cannot modify a closed ticket.'}, status=status.HTTP_400_BAD_REQUEST)
                serializer = TicketSerializer(ticket, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif request.user.is_superuser:  # Allow administrators to modify any ticket
                serializer = TicketSerializer(ticket, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'You can only edit your own ticket.'}, status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        ticket = self.get_ticket(pk)
        if ticket:
            if request.user.is_admin:  # Only allow admins to delete tickets
                ticket.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'You do not have permission to delete this ticket.'},
                                status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_404_NOT_FOUND)
