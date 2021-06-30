import logging
import re

from django.conf import settings 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save, pre_migrate
from django.dispatch.dispatcher import receiver

from .utils import render_template


logger=logging.getLogger(__name__)

# Create your models here.
class SubscriptionQuerySet(models.QuerySet):
    
    def filter(self, *args, **kwargs):
        content_object=kwargs.pop('content_object', None)
        if content_object:
            kwargs['content_type']=ContentType.objects.get_for_model(content_object._meta.model)
            try:
                kwargs['object_id']=int(content_object.pk)
            except ValueError:
                return self.none()
        return super().filter(*args, **kwargs)
    
    def get_or_prepare(self, user, content_object):
        try:
            return self.get(user=user, content_object=content_object)
        except self.model.DoesNotExist:
            return self.model(user=user, content_object=content_object)

class Subscription(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        unique_together=('user', 'content_type', 'object_id')

    objects = SubscriptionQuerySet.as_manager()
    
    def __str__(self):
        return f"{self.user} :-> {self.content_object}"
    
@receiver(post_save)
def notify_subscribers(instance, **kwargs):
    recipients = list(Subscription.objects.filter(
        content_object=instance).values_list("user__email", flat=True))
    if not recipients:
        return
    try:
        send_mail(subject = re.sub(r"\s+", " ", render_template(instance, "title.djtxt")).strip(), 
                  message = render_template(instance, "message.djtxt"), 
                  from_email=settings.DEFAULT_FROM_EMAIL, 
                  recipient_list=recipients, 
                  html_message = render_template(instance, "message.djhtml"),
                  fail_silently=True)
    except Exception:
        logger.exception(f"Exception raised when sending {instance} update notification")

@receiver(pre_migrate)
def disconnect_notify(sender, **kwargs):
    post_save.disconnect(notify_subscribers)