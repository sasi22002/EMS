import logging
from django.core.management.base import BaseCommand, CommandError
from user.models import Role
from utils.enum import RoleEnum

class Command(BaseCommand):
    help = "Command to create a User Roles"
    def handle(self, *args, **options):
        try:            
            """create user roles in Role master table"""
            
            for i in RoleEnum:
                val = Role.objects.update_or_create(role_name=i.name)
                
        except Exception as e:
            logging.info('command not works',e)
            raise CommandError(e)