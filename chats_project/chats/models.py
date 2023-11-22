from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.timezone import localtime


# Create your models here.

class Conversations(models.Model):
    messages = models.TextField(null=False, blank=False)
    type_messages = models.TextField(null=False, blank=False)
    file = models.FileField(null=True)
    user = models.ForeignKey('users.UserCustomer', on_delete=models.PROTECT)
    client = models.ForeignKey('users.Client', on_delete=models.PROTECT)
    is_closed = models.BooleanField(default=False)
    identify = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'conversaciones'
        app_label = 'chats'
        

class HistoryConversations(models.Model):
    messages = models.TextField(null=False, blank=False)
    type_messages = models.TextField(null=False, blank=False)
    file = models.FileField(null=True)
    user = models.ForeignKey('users.UserCustomer', on_delete=models.PROTECT)
    client = models.ForeignKey('users.Client', on_delete=models.PROTECT)
    is_closed = models.BooleanField(default=False)
    identify = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'historial_conversaciones'
        app_label = 'chats'
        

@receiver(post_save, sender=Conversations)
def move_conversation_to_history(sender, instance, created, **kwargs):
    if created:
        history_conversation = HistoryConversations.objects.create(
            messages=instance.messages,
            type_messages=instance.type_messages,
            file=instance.file,
            user=instance.user,
            is_closed=instance.is_closed,
            identify=instance.identify,
            client=instance.client,
            created=instance.created,
            modified=instance.modified
        )
        history_conversation.save()
        
class Catalogue(models.Model):
    name = models.TextField(null=False, blank=False)
    type_catalogue = models.TextField(null=True, blank=False)
    amount = models.TextField()
    images = models.ImageField(upload_to='img_catalogue/', null=True)
    is_enabled = models.BooleanField(default = True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)
    
    class Meta:
        db_table = 'catalogo'
        app_label = 'chats'
        