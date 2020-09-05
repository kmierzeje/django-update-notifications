from .models import Subscription
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.utils.functional import cached_property
from .utils import render_template

class SubscriptionMixin:
    def get(self, request, *args, **kwargs):
        if "subscribe" in request.GET:
            return self.subscribe()
        elif "unsubscribe" in request.GET:
            return self.unsubscribe()
        
        return super().get(request, *args, **kwargs)
    
    def subscribe(self):
        subscription = self.get_subscription()
        if subscription and not subscription.pk:
            subscription.save()
            title = render_template(self.subscription_trigger, "title.djtxt")
            messages.add_message(self.request, messages.INFO, 
                                 f"Successfully subscribed for {title}.")
        return HttpResponseRedirect(self.request.path)
    
    def unsubscribe(self):
        subscription = self.get_subscription()
        if subscription and subscription.pk:
            subscription.delete()
            title = render_template(self.subscription_trigger, "title.djtxt")
            messages.add_message(self.request, messages.INFO, 
                                 f"Successfully unsubscribed {title}.")
        return HttpResponseRedirect(self.request.path)
    
    def get_subscription(self):
        if self.subscription_trigger:
            return Subscription.objects.get_or_prepare(
                user=self.request.user, 
                content_object=self.subscription_trigger)
        else:
            return None
    
    @cached_property
    def subscription_trigger(self):
        return self.get_subscription_trigger()
    
    def get_subscription_trigger(self):
        raise NotImplementedError()
    
    def get_context_data(self, **kwargs):
        return {
                **super().get_context_data(**kwargs),
                'subscription' : self.get_subscription()
            }


