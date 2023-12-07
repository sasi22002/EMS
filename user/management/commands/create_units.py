import logging
from django.core.management.base import BaseCommand, CommandError
from masteradmin.models import UnitMaster
from utils.enum import UnintsEnum

class Command(BaseCommand):
    help = "Command to create a Units"
    def handle(self, *args, **options):
        try:            
            """create units for property details"""
            
            for i in UnintsEnum:
                val = UnitMaster.objects.update_or_create(unit_name=i.value)
                
        except Exception as e:
            logging.info('command not works',e)
            raise CommandError(e)