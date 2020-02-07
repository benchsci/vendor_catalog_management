from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from google.cloud import storage


class UploadView(LoginRequiredMixin, View):

    def post(self, request):
        resumable_upload_url = self._get_resumable_upload_url(request)
        return JsonResponse({'resumable_upload_url': resumable_upload_url})

    def _get_resumable_upload_url(self, request):
        self._client = storage.Client.from_service_account_json(settings.GOOGLE_CLOUD_CREDENTIALS_FILE)
        bucket = self._client.get_bucket(settings.GCS_VENDOR_BUCKET)
        file_size = int(request.POST.get("file_size"))
        vendor = request.POST.get("vendor")
        catalog_name = request.POST.get("catalog_name")
        origin = request.META.get("HTTP_USER_AGENT")
        blob = bucket.get_blob(f"{vendor}/{vendor}_{catalog_name}.csv")
        return blob.create_resumable_upload_session(size=file_size, origin=origin, client=self._client)
