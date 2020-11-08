import requests
import json
import threading
import time
import os
import errno 
from threading import Thread

def printProgressBar (percent_done, prefix = '', suffix = '', decimals = 1, length = 50, fill = '█', printEnd = "\r"):
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
    filledLength = int(length * percent_done/100)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if percent_done == 100: 
        print()

class DownloadClient:

	def __init__(self, base_dir, file_name):

		self.base_dir = base_dir
		self.file_name = file_name
		self.download_path = self.base_dir + self.file_name
		self.bytes_offset = 0
		self.is_paused = False
		self.is_cancelled = False
		self.is_downloading = True

	def writeToFile(self, text) :

		if os.path.exists(self.base_dir):

			if not os.path.isfile(self.download_path):
				file = open(self.download_path, 'w')
			else:	
				file = open(self.download_path, 'r+')
		
			file.seek(self.bytes_offset)
			file.write(text)
			
			return True

		else:
			raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.file_name)


	def start_download(self):

		done = False

		while not done:
			
			#print("Downloading has started")
			receive = requests.get('http://localhost:8000/download', 
									params = {'path' : self.file_name, 'bytes_read' : str(self.bytes_offset)})

			body = json.loads(receive.content)
			text = body['file_content']

			status = self.writeToFile(text)

			self.bytes_offset = int(body["bytes_read"])
			#print(self.bytes_offset)
			done = bool(body['is_complete'])

			printProgressBar(float(body['percentage_done']), prefix = "Progress", suffix = "Complete")

			while self.is_paused:
				time.sleep(1)

			if self.is_cancelled:
				os.remove(self.download_path)
				break

		self.is_downloading = False

	def cancel_download(self):
		self.is_paused = False
		self.is_cancelled = True

	def pause_download(self):
		self.is_paused = True

	def resume_download(self):
		self.is_paused = False


if __name__ == "__main__":

	global downloadFile

	downloadFile = DownloadClient('/home/neel/Atlan/', 'Records.csv') 

	 """
    Usage:

 	input via CLI
        	1   	- 	Required  : Start Download
        	2       - 	Required  : Pause Download
        	3       - 	Required  : Resume Download
        	4       - 	Required  : Abort Download
    """


	while (downloadFile.is_downloading):
		command = input()

		if command == '1':
			thread = Thread(target = downloadFile.start_download)
			thread.start()

		elif command == '2':
			downloadFile.pause_download()

		elif command == '3':
			downloadFile.resume_download()

		elif command == '4':
			downloadFile.cancel_download()
			break

		else:
			print("Please enter a valid command")