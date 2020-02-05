from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/', TemplateView.as_view(template_name="account_login.html")),
    path('', TemplateView.as_view(template_name="translate_index.html")),
]
