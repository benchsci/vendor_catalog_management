from datetime import timedelta
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
        client = storage.Client.from_service_account_json(settings.GOOGLE_CLOUD_CREDENTIALS_FILE)
        bucket = client.get_bucket(settings.GCS_VENDOR_BUCKET)
        file_size = int(request.POST.get("file_size"))
        chunk_size = int(request.POST.get("chunk_size"))
        vendor = request.POST.get("vendor")
        file_name = request.POST.get("file_name")
        origin = request.META.get("HTTP_ORIGIN")
        blob = bucket.blob(f"vendors/{vendor}/{vendor}_{file_name}", chunk_size=chunk_size)
        return blob.create_resumable_upload_session(size=file_size, origin=origin, client=client)


class ListVendorFilesView(LoginRequiredMixin, View):

    def get(self, request):
        vendor_files = self._get_vendor_files(request)
        return JsonResponse({'vendor_files': vendor_files})

    def _get_vendor_files(self, request):
        client = storage.Client.from_service_account_json(settings.GOOGLE_CLOUD_CREDENTIALS_FILE)
        bucket = client.get_bucket(settings.GCS_VENDOR_BUCKET)
        vendor = request.GET.get("vendor")
        blobs = bucket.list_blobs(prefix=f"vendors/{vendor}/{vendor}_")
        vendor_files = list(map(lambda blob: blob.name.rsplit('/', 1)[1].split('_', 1)[1], blobs))
        return vendor_files


class DownloadView(LoginRequiredMixin, View):

    def get(self, request):
        signed_download_url = self._get_signed_download_url(request)
        return JsonResponse({"signed_download_url": signed_download_url})

    def _get_signed_download_url(self, request):
        client = storage.Client.from_service_account_json(settings.GOOGLE_CLOUD_CREDENTIALS_FILE)
        bucket = client.get_bucket(settings.GCS_VENDOR_BUCKET)
        vendor = request.GET.get("vendor")
        file_name = request.GET.get("file_name")
        blob = bucket.blob(f"vendors/{vendor}/{vendor}_{file_name}")
        return blob.generate_signed_url(expiration=timedelta(minutes=30))
