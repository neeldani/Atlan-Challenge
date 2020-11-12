# Atlan-Challenge

## Description
This project provides a set of REST API endpoints to pause, resume and abort a huge file upload, download as well as a long running server process. This would essentially prevent waste of server's resources in case of wrong uploads/ downloads, reducing the load by avoiding unecessary computation. The idea for this implementation has been somewhat drawn from the resumable.js library and the tus protocol.

## Installation
```
git clone https://github.com/neeldani/Atlan-Challenge.git
cd Atlan-Challenge
```

### To run server using docker
``` 
docker build .
docker-compose up
```

### To run on local
```
cd Challenge
python manage.py runserver
```

## Running client
Since the methodology for resumable upload and download requires multiple POST and GET requests respectively, an implementation of clients for the download as well as the upload process has been provided. This essentially abstracts the multiple GET/ POST requests that the client needs to make to the server in order to completely download/ upload a file.

### To run download client
Run the DownloadClient.py script present in the Atlan-Challenge directory
```
python DownloadClient.py
```

### To run upload client
Run the UploadClient.py. script present in the Atlan-Challenge directory
```
python UploadClient.py
```
### Options on running the client program
| CLI Input | Description |
| :--- | :--- |
| 1 | Start Upload/ Download |
| 2 | Pause Upload/ Download |
| 3 | Resume Upload/ Download |
| 4 | Abort Upload/ Download |


## Resumable Process

Request | Endpoint      | Description                       |
|:-----------|:----------------------------------------------------------------|:----------------------------------|
|GET | `{id}/process/`        | starts running a long process |
|POST | `{id}/process/pause/` | pause long running process |
|POST | `{id}/process/cancel/` | cancel long running process |
|POST | `{id}/process/resume/` | resume a list of valid work types |

### Methodology
The client makes the `GET` request in order to start the long running process. The main thread dispatches a worker thread to tend to the request. The main thread exits with a response while the worker thread continues to run the process in background. This prevents timeouts. While the worker thread runs, a `POST` request can be made to pause, cancel and resume the process. 


## Resumable Download

Request | Endpoint                                                               | Description                       |
|:-----------|:------------------------------------------------------------------|:----------------------------------|
|GET | `download/?file_name={file_name}&bytes_read={bytes_read}` | file_name (**reqd**) should be a valid file name present at the server's Files directory and (**bytes_read**) should be an integer  |

### Reponse

```javascript
{
  "file_content" : str,
  "bytes_read" : int,
  "is_complete" : bool
}
```

### Methodology
The client makes multiple `GET` requests to the server. The server reads a chunk of file (no. of bytes which can be configured in settings.py) and returns the read `file_content` and the `bytes_read`. The client then makes the next `GET` request with the earlier received `bytes_read` param value and the server returns the next block of bytes. For all such requests, the `is_complete` param value is set to False. When the download process completes, the `is_complete` param is set to True indicating download is now complete.


## Resumable Upload

Request | Endpoint                                                               | Description                       |
|:-----------|:---------------------------------------------------------------------|:----------------------------------|
|GET | `upload/?file_name={file_name}&bytes_read={bytes_read}/` | file_name (**reqd**) should be a valid file name present at the server's Files directory and (**bytes_read**) should be an integer.  |
|POST | `upload/cancel/?file_name={file_name}/` | file_name (**reqd**) which is being currently uploaded  |

### Reponse

```javascript
{
  "bytes_read" : int,
}
```

### Methodology
The client makes multiple `POST` requests to the server. The client reads a block of file which it sends to the server as `text`. The server reads the `POST request body` and then sends the number of bytes read to the client. While the upload is taking place, the client can pause and cancel the upload. In case of an upload cancel, a `POST` request is sent to the server to delete the intermediate file formed due to the ongoing upload process.


## Status Codes
| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |


## References
[GitHub Atlan Challenge](https://github.com/Manvityagi/Atlan-Challenge---Long-Running-Task-Manager)
</br>
[Resumable.js](http://resumablejs.com/)
</br>
[tus](https://github.com/tus/tusd)
