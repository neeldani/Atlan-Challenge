import os
import json
from rest_framework.response import Response

from download.config import FILE_DIRECTORY


class UploadManager:

    def __init__(self, file_name, bytes_read):
        self.file_path = os.path.join(FILE_DIRECTORY, file_name)
        self.bytes_read = bytes_read
        super().__init__()

    def start_upload(self, text):

        if not os.path.isfile(self.file_path):
            file = open(self.file_path, 'w')
        else:
            file = open(self.file_path, 'r+')

        file.seek(self.bytes_read)
        print(text)
        file.write(text)
        self.bytes_read = self.bytes_read + len(text)
        file.close()

        dict_response = {
            'bytes_read': self.bytes_read
        }

        return Response(dict_response, 200)


