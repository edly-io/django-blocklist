"""Update blocklist with new IPs, or set metadata on existing IPs."""
import logging

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import validate_ipv46_address

from ...models import BlockedIP
from ...utils import COOLDOWN


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("ips", nargs="+", type=str, help="IPs (space-separated)")
        parser.add_argument(
            "--cooldown",
            help=f"Days with no requests before IP is dropped from blocklist (default: {COOLDOWN})",
        )
        parser.add_argument("--reason", help="'reason' field value for these IPs", default="")

    help = __doc__

    def handle(self, *args, **options):
        ips = options.get("ips")
        cooldown = options.get("cooldown")
        reason = options.get("reason")
        for ip in ips:
            try:
                validate_ipv46_address(ip)
            except ValidationError:
                print(f"Invalid IP: {ip}")
                continue
            entry, created = BlockedIP.objects.get_or_create(ip=ip)
            updated = []
            if reason and entry.reason != reason:
                entry.reason = reason
                updated.append("reason")
            if cooldown and entry.cooldown != (cooldown := int(cooldown)):
                entry.cooldown = cooldown
                updated.append("cooldown")
            if updated or created:
                entry.save()
                summary = "Created entry" if created else f"Updated {' and '.join(updated)}"
                print(f"{summary} for {ip}")
