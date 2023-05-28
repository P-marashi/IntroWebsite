from django.urls import path
from .views import (
    TicketListCreateAPIView,
    TicketDetailAPIView,
    AnswerListCreateAPIView,
    AnswerDetailAPIView
)

urlpatterns = [
    # Ticket URLs
    path('tickets/', TicketListCreateAPIView.as_view(), name='ticket-list-create'),
    path('tickets/<int:pk>/', TicketDetailAPIView.as_view(), name='ticket-detail'),

    # Answer URLs
    path('answers/', AnswerListCreateAPIView.as_view(), name='answer-list-create'),
    path('answers/<int:pk>/', AnswerDetailAPIView.as_view(), name='answer-detail'),
]
