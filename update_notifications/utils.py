from django.template.loader import render_to_string
from django.conf import settings

def render_template(instance, name):
    return render_to_string(
        f"{instance._meta.app_label}/notifications/{instance._meta.object_name.lower()}/{name}",
        {
            "object" : instance,
            'site_url' : settings.REQUEST_BASE_URL
        })