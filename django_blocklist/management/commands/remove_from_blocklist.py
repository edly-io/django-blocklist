"""Remove given IPs from blocklist."""
import datetime
import logging
import sys

from django.conf import settings
from django.core.management.base import BaseCommand

from blocklist.models import BlockedIP

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("ips", nargs="+", type=str, help="IPs (space-separated) to remove")

    help = __doc__

    def handle(self, *args, **options):
        ips = options.get("ips")
        matches = BlockedIP.objects.filter(ip__in=ips)
        count = matches.count()
        print(f"Found {count} of {len(ips)}.")
        if count:
            matches.delete()
            print("Deleted.")