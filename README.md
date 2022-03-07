# Django-blocklist

A reusable Django app that implements IP-based blocklisting. It consists of a data model for the blocklist entries, and middleware that performs the blocking. It is mostly controlled by its management commands.

This app is primarily intended for use in situations where server-level blocking is not available, e.g. on platform-as-a-service hosts like PythonAnywhere or Heroku. Being an application-layer solution, it's not as performant as blocking via firewall or web server process, but is suitable for moderate traffic sites. It also offers better developer/operator ergonomics, and integration with the application stack for easier management.

## Quick start

1. Add "blocklist" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        "blocklist",
    ]

2. Add the middleware like this::

    MIDDLEWARE = [
        ...
       "blocklist.middleware.BlocklistMiddleware",
    ]

3. Add settings (all optional)::

   BLOCKLIST_CONFIG = {
       "cooldown": 7,  # Number of days that it takes an IP to expire from the blocklist
       "cache-ttl": 600,  # Seconds that the blocklist is cached after being read from the database
       "denial-template": "Your IP address {ip} has been blocked for violating our Terms of Service. IP will be unblocked after {cooldown} days."
   }

4. Run ``python manage.py migrate`` to create the BlockedIP model.

## Management commands

Django-blocklist includes several management commands:

* `add_to_blocklist` &mdash; (one or more IPs)
* `import_blocklist` &mdash; convenience command for importing an existing list
* `remove_from_blocklist` &mdash; (one or more IPs)
* `search_blocklist` &mdash; look for an IP in the list; in addition to info on stdout, returns an exit code of 0 if successful
* `update_blocklist` &mdash; change the `reason` or `cooldown` values for existing entries
* `report_blocklist` &mdash; useful information on the current collection of entries
* `clean_blocklist` &mdash; remove entries that have fulfilled their `cooldown` period

The `--help` for each of these details its available options.

For exporting or importing blocklist data, use Django's built-in `dumpdata` and `loaddata` management commands.

## Reporting

The `report_blocklist` command gives information about the current collection of entries, including:
* Total requests blocked
* Entries in blocklist
* Active in last 24 hours
* Stale (added over 24h ago and not seen since)
* Most active
* Most recent
* Longest lived
* IP counts by reason
