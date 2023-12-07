import pytz
import datetime
import pytest
import unittest

from ..models import BlockedIP


@pytest.mark.django_db
class CommandsTest(unittest.TestCase):
    def setUp(self):
        BlockedIP.objects.all().delete()
        self.ip1 = "1.1.1.1"
    
    def test_days_left(self):
        two_days_ago = datetime.datetime.now(pytz.UTC) - datetime.timedelta(days=2)
        BlockedIP.objects.create(ip=self.ip1, cooldown=3, last_seen=two_days_ago)
        entry = BlockedIP.objects.get(ip=self.ip1)
        remaining = entry.cooldown - (datetime.datetime.now(pytz.UTC) - entry.last_seen).days
        self.assertEqual(remaining, 1)
