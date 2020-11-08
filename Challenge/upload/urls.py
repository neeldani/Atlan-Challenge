from django.urls import path

from .controllers.upload import UploadStartController

urlpatterns = [
    path("", UploadStartController.as_view(), name="Upload_start")
]
