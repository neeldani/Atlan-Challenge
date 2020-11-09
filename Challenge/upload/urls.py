from django.urls import path

from .controllers.upload import UploadStartController, UploadCancelController

urlpatterns = [
    path("", UploadStartController.as_view(), name="Upload_start"),
    path("cancel", UploadCancelController.as_view(), name="Upload_cancel")
]
