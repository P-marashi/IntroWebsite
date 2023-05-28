from django.contrib import admin
from .models import Ticket, Answer


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # Displayed fields in the list view of the admin interface
    list_display = ('title', 'user', 'created', 'updated_at')

    # Filter options for the list view
    list_filter = ('created', 'updated_at')

    # Fields to enable searching in the admin interface
    search_fields = ('title', 'user__username')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    # Displayed fields in the list view of the admin interface
    list_display = ('ticket', 'admin', 'status', 'created_at')

    # Filter options for the list view
    list_filter = ('status', 'created_at')

    # Fields to enable searching in the admin interface
    search_fields = ('ticket__title', 'admin__username')
