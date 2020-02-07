from django.contrib import admin
from django.contrib.auth.views import login_required
from django.urls import path, include
from django.views.generic import TemplateView

from benchsci.vendor_catalog.library_translation.views import UploadView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", TemplateView.as_view(template_name="vendor_catalog_login.html")),
    path("auth/", include("social_django.urls", namespace="social")),
    path("auth/", include("django.contrib.auth.urls")),
    path("upload/", UploadView.as_view()),
    path("", login_required(TemplateView.as_view(template_name="vendor_catalog_index.html"))),
]
