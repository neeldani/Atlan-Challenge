from threading import Thread

from rest_framework.response import Response
from rest_framework.views import APIView

from download.Manager.manager import DownloadManager


class DownloadStartController(APIView):

    def get(self, request):

        file_path = request.query_params['file_name']
        bytes_read = int(request.query_params['bytes_read'])
        manager = DownloadManager(file_path, bytes_read)

        if manager.start_download():
            return Response(manager.response(), status=200)
        else:
            return Response(status=400)
