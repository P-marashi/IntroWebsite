from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """ Ticket model on admin interface """

    # Displayed fields in the list view of the admin interface
    list_display = ('title', 'user', 'created_at', 'updated_at')

    # Filter options for the list view
    list_filter = ('created_at', 'updated_at')

    # Fields to enable searching in the admin interface
    search_fields = ('title', 'user__username')



