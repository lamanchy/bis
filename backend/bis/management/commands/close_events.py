from datetime import timedelta

from dateutil.utils import today
from django.core.management.base import BaseCommand

from bis.emails import email_event_closed
from event.models import Event


class Command(BaseCommand):
    def handle(self, *args, **options):
        for event in Event.objects.filter(end__lt=today().date() - timedelta(days=20), is_closed=False):
            event.is_closed = True
            event.save()

            email_event_closed(event, True)
