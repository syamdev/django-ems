# anthology/apps.py
#
# from rock_n_roll.apps import RockNRollConfig
#
# class JazzManoucheConfig(RockNRollConfig):
#     verbose_name = "Jazz Manouche"
#
# # anthology/settings.py
#
# INSTALLED_APPS = [
#     'anthology.apps.JazzManoucheConfig',
#     # ...
# ]

from django.apps import AppConfig


class AppEmsConfig(AppConfig):
    name = 'app_ems'
    verbose_name = 'EMS Section'
