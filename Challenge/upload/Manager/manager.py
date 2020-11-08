import os
from download.config import FILE_DIRECTORY


class UploadManager:

    def __init__(self, file_name, bytes_read, text):
        self.file_path = os.path.join(FILE_DIRECTORY, file_name)
        self.bytes_read = bytes_read
        self.text = text
        super().__init__()

    def start_upload(self):

        print(self.text)
        if not os.path.isfile(self.file_path):
            file = open(self.file_path, 'w')
        else:
            file = open(self.file_path, 'r+')

        file.seek(self.bytes_read)
        file.write(self.text)
        file.close()

    def response(self):

        dict_response = {
            'bytes_read': self.bytes_read + len(self.text)
        }
        print(dict_response)
        return dict_response
