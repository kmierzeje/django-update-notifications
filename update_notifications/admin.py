from django.contrib import admin

from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display=('content_object', 'user')
    list_filter=('user',)
