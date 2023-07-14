import pytest
from intro.tickets.models import Ticket


@pytest.fixture
def ticket():
    ticket = Ticket.objects.create(
        title='Test Ticket',
        description='This is a test ticket',
    )
    return ticket


@pytest.mark.django_db
def test_ticket_model_str(ticket):
    # Test the __str__ method of the Ticket model
    expected_str = f"Test Ticket - None"
    assert str(ticket) == expected_str


@pytest.mark.django_db
def test_ticket_status_default_value(ticket):
    # Test the default value of the status field
    assert ticket.status == 'active'


@pytest.mark.django_db
def test_ticket_creation_without_optional_fields():
    # Test ticket creation without optional fields
    ticket = Ticket.objects.create(
        title='Test Ticket without Optional Fields',
        description='This ticket does not have optional fields',
    )
    assert ticket.file == ''
    assert ticket.image is None


@pytest.mark.django_db
def test_ticket_replieds_relationship(ticket):
    # Test the relationship between a ticket and its replies
    reply = Ticket.objects.create(
        parent=ticket,
        title='Reply Ticket',
        description='This is a reply to the parent ticket',
    )
    assert reply.parent == ticket
    assert ticket.replieds.count() == 1
    assert ticket.replieds.first() == reply
