from django.urls import path

from process.controller.process import ProcessStartController, ProcessPauseController, ProcessStopController, \
    ProcessResumeController

urlpatterns = [
    path("", ProcessStartController.as_view(), name="Process_start"),
    path("pause", ProcessPauseController.as_view(), name="Process_pause"),
    path("cancel", ProcessStopController.as_view(), name="Process_stop"),
    path("resume", ProcessResumeController.as_view(), name="Process_resume")
]