import requests
import json
import threading
import time
import os
import errno
from threading import Thread


def printProgressBar(percent_done, prefix='', suffix='', decimals=1, length=50, fill='█', printEnd="\r"):
    """
	Call in a loop to create terminal progress bar
	@params:
		iteration   - Required  : current iteration (Int)
		total       - Required  : total iterations (Int)
		prefix      - Optional  : prefix string (Str)
		suffix      - Optional  : suffix string (Str)
		decimals    - Optional  : positive number of decimals in percent complete (Int)
		length      - Optional  : character length of bar (Int)
		fill        - Optional  : bar fill character (Str)
		printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
	"""
    percent = ("{0:." + str(decimals) + "f}").format(percent_done)
    filledLength = int(length * percent_done / 100)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if percent_done == 100:
        print()


class UploadClient:

    def __init__(self, file_path, chunk_size):

        self.chunk_size = chunk_size
        self.file_path = file_path
        self.file_name = os.path.split(file_path)[1]
        self.size = os.path.getsize(self.file_path)
        self.bytes_offset = 0
        self.is_paused = False
        self.is_cancelled = False
        self.is_uploading = True

    def read_from_file(self):

        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.file_path)
        else:
            file = open(self.file_path, 'r')

        file.seek(self.bytes_offset)
        text = file.read(self.chunk_size)
        return text

    def start_upload(self):

        done = False

        while not done:

            text = self.read_from_file()

            # print("Downloading has started")
            receive = requests.post('http://localhost:8000/upload/',
                                    params={'file_name': self.file_name, 'bytes_read': str(self.bytes_offset)},
                                    data={'text': str(text)})

            self.bytes_offset = self.bytes_offset + self.chunk_size

            if self.bytes_offset > self.size:
                done = True

            printProgressBar(min(self.bytes_offset * 100 / float(self.size), 100), prefix="Progress", suffix="Complete")

            while self.is_paused:
                time.sleep(1)

            if self.is_cancelled:
                requests.post('http://localhost:8000/upload/cancel/',
                              params={'file_name': self.file_name})
                break

        self.is_uploading = False

    def cancel_upload(self):
        self.is_paused = False
        self.is_cancelled = True

    def pause_upload(self):
        self.is_paused = True

    def resume_upload(self):
        self.is_paused = False


if __name__ == "__main__":

    global uploadFile
   
    uploadFile = UploadClient(os.path.join(os.getcwd(), 'Upload.csv'), 5000)

    instructions = {1: "Start Upload",
                    2: "Pause",
                    3: "Resume",
                    4: "Abort",
                    5: "Exit program"
                    }

    print("{:<25} {:<10}".format('Input Command CLI', 'Action'))

    for k, v in instructions.items():
        print("{:<25} {:<10}".format(k, v))

    while uploadFile.is_uploading:
        command = input()

        if command == '1':
            thread = Thread(target=uploadFile.start_upload)
            thread.start()

        elif command == '2':
            uploadFile.pause_upload()

        elif command == '3':
            uploadFile.resume_upload()

        elif command == '4':
            uploadFile.cancel_upload()
            break

        elif command == '5':
            break

        else:
            print("Please enter a valid command")
