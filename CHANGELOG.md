# Django-Blocklist Changelog

## 2023-01-25
### v1.4.0
* Added --reason option on report_blocklist

## 2022-12-10
### v1.3.3, v1.3.4
* Minor bugfixes
### v1.3.2
* "Most active" section of report now sorts by, and shows, rate per hour

## 2022-11-20
### v1.3.1
* Middleware now only runs when `settings.DEBUG` is `False`

## 2022-08-08
### v1.3.0
* Replaced `add_to_blocklist` command with expanded `update_blocklist`
* Removed `--last-seen` option from `update_blocklist`

## 2022-08-07
### v1.2.3
* Fixed bug in "Most recent" report section
* Updated sample report and linked from README

## 2022-07-10
### v1.2.2
* Moved to GitLab. No internal changes except updating project URL in config files.

## 2022-07-09
### v1.2.1
* Added requirements files
* Updated project config files to indicate Django 4 compatibility
* Fixed exception handling that caused noise in error-tracking tools
* Minor README edits

## 2022-07-02
### v1.2.0
* Changed default tally to 0
* Added tally to admin list view

## 2022-06-18
### v1.1.0
* Added scaffolding to allow tests to run standalone (outside a project) via `pytest`.
* Updated packaging info to indicate Django 4 compatibility.

## 2022-03-28
### v1.0.3
Minor cleanup of imports.

## 2022-03-18
### v1.0.2
Minor cleanup; expanded README.

## 2022-03-16
### v1.0.1
Initial release.
