from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime


# Create your models here.
class Conversations(models.Model):
    messages = models.TextField(null=False, blank=False)
    type_messages = models.TextField(null=False, blank=False)
    file = models.TextField(null=True, blank=False)
    user = models.ForeignKey('users.UserCustomer', on_delete=models.PROTECT)
    client = models.ForeignKey('users.Client', on_delete=models.PROTECT)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'conversaciones'
        app_label = 'chats'

class HistoryConversations(models.Model):
    messages = models.TextField(null=False, blank=False)
    type_messages = models.TextField(null=False, blank=False)
    file = models.TextField(null=True, blank=False)
    user = models.ForeignKey('users.UserCustomer', on_delete=models.PROTECT)
    client = models.ForeignKey('users.Client', on_delete=models.PROTECT)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'historial_conversaciones'
        app_label = 'chats'
        
class Catalogue(models.Model):
    name = models.TextField(null=False, blank=False)
    type_catalogue = models.TextField(null=False, blank=False)
    amount = models.TextField()
    is_enabled = models.BooleanField(default = True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)
    
    class Meta:
        db_table = 'catalogo'
        app_label = 'chats'
        
