from django.conf import settings
import os

# define max chunk size in bytes
CHUNK_SIZE = 5000

# define deafault download directory path
FILE_DIRECTORY = os.path.join(settings.BASE_DIR, 'Files')