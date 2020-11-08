import os
from download.config import FILE_DIRECTORY
from download.config import CHUNK_SIZE


class DownloadManager:

    def __init__(self, file_name, bytes_read):
        self.file_path = os.path.join(FILE_DIRECTORY, file_name)
        self.bytes_read = bytes_read
        self.chunk_size = CHUNK_SIZE  # in bytes
        self.text = ""
        self.done = False
        self.percentage_done = 0
        super().__init__()

    def start_download(self):

        if os.path.isfile(self.file_path):

            file_size = os.path.getsize(self.file_path)
            print(file_size)
            file = open(self.file_path, 'r')
            file.seek(self.bytes_read)
            self.text = file.read(self.chunk_size)

            if self.bytes_read + self.chunk_size > file_size:
                self.bytes_read = self.bytes_read + file_size - self.bytes_read
                self.done = True
            else:
                self.bytes_read = self.bytes_read + self.chunk_size

            self.percentage_done = self.bytes_read * 100 / file_size
            file.close()
            return True
        else:
            return False

    def response(self):
        dict_response = {
            'bytes_read': self.bytes_read,
            'file_content': self.text,
            'is_complete': self.done,
            'percentage_done': self.percentage_done
        }
        print(dict_response)
        return dict_response
