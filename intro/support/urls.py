from django.urls import path
from .apis import (
    TicketListCreateView,
    TicketDetailView,
)

urlpatterns = [
    # Ticket URLs
    path('tickets/', TicketListCreateView.as_view(), name='ticket-list-create'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),

]
