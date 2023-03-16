import datetime
import pytest
import sys
import unittest
from django.core.management import call_command
from io import StringIO

from ..models import BlockedIP


@pytest.mark.django_db
class CommandsTest(unittest.TestCase):
    def setUp(self):
        BlockedIP.objects.all().delete()

    def tearDown(self):
        BlockedIP.objects.all().delete()

    def test_clean(self):
        two_days_ago = datetime.datetime.now() - datetime.timedelta(days=2)
        BlockedIP.objects.create(ip="1.1.1.1", cooldown=1, last_seen=two_days_ago)
        BlockedIP.objects.create(ip="2.2.2.2", cooldown=3, last_seen=two_days_ago)
        # We now have two IPs
        assert BlockedIP.objects.count() == 2
        # Running clean_blocklist with --dry-run doesn't delete one
        call_command("clean_blocklist", verbosity=0, dry_run=1)
        self.assertEqual(BlockedIP.objects.count(), 2)
        # Running clean_blocklist does delete one
        call_command("clean_blocklist", verbosity=0)
        self.assertEqual(BlockedIP.objects.count(), 1)
        # The one that should still be there, is still there
        self.assertTrue(BlockedIP.objects.filter(ip="2.2.2.2").exists())

    def test_add(self):
        call_command("update_blocklist", "3.3.3.3", verbosity=0)
        self.assertTrue(BlockedIP.objects.filter(ip="3.3.3.3").exists())

    def test_remove(self):
        BlockedIP.objects.create(ip="4.4.4.4")
        call_command("remove_from_blocklist", "4.4.4.4", verbosity=0)
        self.assertEqual(BlockedIP.objects.filter(ip="4.4.4.4").count(), 0)

    def test_add_invalid(self):
        sys.stdout = (out := StringIO())
        bad_ip = "foo"
        call_command("update_blocklist", bad_ip, verbosity=0)
        self.assertIn("Invalid", out.getvalue())

    def test_update(self):
        BlockedIP.objects.create(ip="5.5.5.5", reason="R1", cooldown=1)
        call_command("update_blocklist", "5.5.5.5", reason="R2", cooldown=2)
        entry = BlockedIP.objects.get(ip="5.5.5.5")
        self.assertEqual(entry.reason, "R2")
        self.assertEqual(entry.cooldown, 2)

    def test_update_creation_message(self):
        """Newly created entry should be reported"""
        sys.stdout = (out := StringIO())
        call_command("update_blocklist", "5.5.6.6")
        self.assertIn("Created", out.getvalue())

    def test_update_changed_message(self):
        """If we update both fields, output should say so"""
        sys.stdout = (out := StringIO())
        BlockedIP.objects.create(ip="6.6.6.6", reason="R1", cooldown=1)
        call_command("update_blocklist", "6.6.6.6", reason="R2", cooldown=2)
        self.assertIn("reason and cooldown", out.getvalue())

    def test_update_no_message_if_no_change(self):
        """If we 'update' with the existing values, IP shouldn't show in output"""
        sys.stdout = (out := StringIO())
        BlockedIP.objects.create(ip="7.7.7.7", reason="R1", cooldown=1)
        call_command("update_blocklist", "7.7.7.7", reason="R1", cooldown=1)
        self.assertNotIn("7.7.7.7", out.getvalue())

    def test_report(self):
        sys.stdout = (out := StringIO())
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)
        BlockedIP.objects.create(ip="8.8.8.8", first_seen=yesterday, last_seen=today)
        BlockedIP.objects.create(ip="9.9.9.9", first_seen=yesterday, last_seen=today, tally=240)
        call_command("report_blocklist")
        result = out.getvalue()
        self.assertIn("8.8.8.8 -- 0 blocks", result)
        self.assertIn("10 per hour", result)

    def test_reason_report(self):
        sys.stdout = (out := StringIO())
        reasons = ["A", "B"]
        for n, reason in enumerate(reasons):
            BlockedIP.objects.create(ip=f"{n}.{n}.{n}.{n}", reason=reason)
        call_command("report_blocklist", reason=reasons[0])
        result = out.getvalue()
        assert BlockedIP.objects.count() == 2
        self.assertIn("Entries in blocklist: 1", result)
