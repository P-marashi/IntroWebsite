from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import Http404
from .models import Ticket, Answer
from .serializers import TicketSerializer, AnswerSerializer


class TicketListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handles GET request to retrieve a list of tickets.
        If the user is a superuser, all tickets are returned.
        Otherwise, only tickets belonging to the authenticated user are returned.
        """
        if request.user.is_superuser:
            tickets = Ticket.objects.all()
        else:
            tickets = Ticket.objects.filter(user=request.user)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Handles POST request to create a new ticket.
        The user is set as the authenticated user.
        """
        serializer = TicketSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to get the ticket object by its primary key (pk).
        Raises a 404 error if the ticket is not found or if the user does not have permission to access it.
        """
        try:
            ticket = Ticket.objects.get(pk=pk)
            # Check if the user is the owner or admin
            if ticket.user == self.request.user or self.request.user.is_superuser:
                return ticket
            else:
                raise Http404
        except Ticket.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Handles GET request to retrieve details of a specific ticket.
        Only the owner of the ticket or an admin can access it.
        """
        ticket = self.get_object(pk)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Handles PUT request to update a specific ticket.
        Only the owner of the ticket or an admin can update it.
        """
        ticket = self.get_object(pk)
        serializer = TicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Handles DELETE request to delete a specific ticket.
        Only an admin can delete a ticket.
        """
        ticket = self.get_object(pk)
        if request.user.is_superuser:  # Check if the user is an admin
            ticket.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"message": "Only admin users can delete tickets."},
                status=status.HTTP_403_FORBIDDEN,
            )


class AnswerListCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        Handles GET request to retrieve a list of answers.
        Only accessible by admin users.
        """
        answers = Answer.objects.all()
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Handles POST request to create a new answer.
        Only accessible by admin users.
        """
        serializer = AnswerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        """
        Helper method to get the answer object by its primary key (pk).
        Raises a 404 error if the answer is not found.
        """
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Handles GET request to retrieve details of a specific answer.
        Only accessible by admin users.
        """
        answer = self.get_object(pk)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Handles PUT request to update a specific answer.
        Only accessible by admin users.
        """
        answer = self.get_object(pk)
        serializer = AnswerSerializer(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Handles DELETE request to delete a specific answer.
        Only accessible by admin users.
        """
        answer = self.get_object(pk)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
