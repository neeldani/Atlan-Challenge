from threading import Thread

from rest_framework.response import Response
from rest_framework.views import APIView

from upload.Manager.manager import UploadManager


class UploadStartController(APIView):

    def post(self, request):
        file_path = request.query_params['path']
        bytes_read = int(request.query_params['bytes_read'])
        text = request.data
        manager = UploadManager(file_path, bytes_read, text)

        manager.start_upload()
        return Response(manager.response(), status=200)
