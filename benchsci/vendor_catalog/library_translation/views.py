from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from google.cloud import storage

from benchsci.vendor_catalog.library_translation.backend.bsproduct.packaging import (
    generate_translation_lists_files,
)


def get_translation_table_file_name(vendor_catalog_file_name):
    vendor_catalog_file_name_prefix, extension = vendor_catalog_file_name.rsplit('.', 1)
    return f"{vendor_catalog_file_name_prefix}_translation_rules.{extension}"

class UploadView(LoginRequiredMixin, View):

    def post(self, request):
        if request.POST.get("internal"):
            return self._backend_upload(request)
        blob = self._get_gcs_blob(request)
        origin = request.META.get("HTTP_ORIGIN")
        file_size = int(request.POST.get("file_size"))
        resumable_upload_url = blob.create_resumable_upload_session(size=file_size, origin=origin)
        return JsonResponse({'resumable_upload_url': resumable_upload_url})

    def _backend_upload(self, request):
        try:
            request.POST = request.POST.copy()
            file_name = get_translation_table_file_name(request.POST.get("file_name"))
            request.POST["file_name"] = file_name
            blob = self._get_gcs_blob(request)
            blob.upload_from_filename(Path(settings.TRANSLATION_LOCATION, file_name))
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def _get_gcs_blob(self, request):
        client = storage.Client.from_service_account_json(settings.GOOGLE_CLOUD_CREDENTIALS_FILE)
        bucket = client.get_bucket(settings.GCS_VENDOR_BUCKET)
        chunk_size_string = request.POST.get("chunk_size")
        chunk_size = int(chunk_size_string) if chunk_size_string else None
        vendor = request.POST.get("vendor")
        file_name = request.POST.get("file_name")
        return bucket.blob(f"vendors/{vendor}/{vendor}_{file_name}", chunk_size=chunk_size)


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
        if request.GET.get("internal"):
            return self._backend_download(request)
        blob = self._get_gcs_blob(request)
        signed_download_url = blob.generate_signed_url(expiration=timedelta(minutes=30))
        return JsonResponse({"signed_download_url": signed_download_url})

    def _backend_download(self, request):
        blob = self._get_gcs_blob(request)
        file_name = request.GET.get("file_name")
        try:
            blob.download_to_filename(Path(settings.TRANSLATION_LOCATION, file_name))
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def _get_gcs_blob(self, request):
        client = storage.Client.from_service_account_json(settings.GOOGLE_CLOUD_CREDENTIALS_FILE)
        bucket = client.get_bucket(settings.GCS_VENDOR_BUCKET)
        vendor = request.GET.get("vendor")
        file_name = request.GET.get("file_name")
        return bucket.blob(f"vendors/{vendor}/{vendor}_{file_name}") 


class GenerateTranslationView(LoginRequiredMixin, View):

    def post(self, request):
        try:
            file_name = request.POST.get("file_name")
            catalog_file_path = str(Path(settings.TRANSLATION_LOCATION, file_name))
            translation_table_path = get_translation_table_file_name(catalog_file_path)
            translation_database_path = Path(Path(__file__).resolve().parent, "tests", "data", "translation_database.txt")
            generate_translation_lists_files(catalog_file_path, translation_database_path, translation_table_path)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
