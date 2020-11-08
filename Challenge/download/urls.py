from django.urls import path

from .controllers.download import DownloadStartController

urlpatterns = [
    path("", DownloadStartController.as_view(), name="Download_Start")
]
