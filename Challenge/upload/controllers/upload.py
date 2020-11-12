from threading import Thread

from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
import os

from upload.Manager.manager import UploadManager


class UploadStartController(APIView):

    def post(self, request):
        bytes_read = int(request.query_params['bytes_read'])
        file_name = request.query_params['file_name']
        text = request.data['text']

        manager = UploadManager(file_name, bytes_read)

        return manager.start_upload(text)

class UploadCancelController(APIView):

    def post(self, request):
        from download.config import FILE_DIRECTORY
        path = os.path.join(FILE_DIRECTORY, request.query_params['file_name'])

        if os.path.isfile(path):
            os.remove(path)
