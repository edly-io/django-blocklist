#!/usr/bin/env python
"""
This script to makes it easier to run tests and manage migrations when working on django-blocklist outside of a Django project.

To run the script, specify DJANGO_SETTINGS_MODULE, e.g.:

    DJANGO_SETTINGS_MODULE=settings ./manage.py
"""
import os
import django
import sys
from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

django.setup()
execute_from_command_line(sys.argv)
