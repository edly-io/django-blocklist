#!/usr/bin/env python
"""Special script to make it easier to run tests and manage migrations."""

import django
import sys
from django.core.management import execute_from_command_line

django.setup()
execute_from_command_line(sys.argv)
