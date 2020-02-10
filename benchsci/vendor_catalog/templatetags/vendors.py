from django import template
from django.conf import settings
from django.utils.datastructures import OrderedSet
from google.cloud import storage

register = template.Library()


@register.inclusion_tag('select_vendors.html')
def select_vendors():
    client = storage.Client.from_service_account_json(settings.GOOGLE_CLOUD_CREDENTIALS_FILE)
    bucket = client.get_bucket(settings.GCS_VENDOR_BUCKET)
    blobs = bucket.list_blobs()
    vendors = OrderedSet()
    for blob in blobs:
        vendors.add(blob.name.split('/')[1])
    return {'vendors': vendors}
