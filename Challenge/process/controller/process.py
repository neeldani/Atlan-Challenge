from rest_framework.response import Response
from rest_framework.views import APIView

from process.Manager.manager import ProcessManager


class ObjectMapper:
    mapper = {}

    @classmethod
    def get_manager(self, id, create_new_object):

        if id in self.mapper:
            return self.mapper[id]

        elif create_new_object:
            manager = ProcessManager()
            self.mapper[id] = manager
            return manager

        else:
            return None

    @classmethod
    def remove_manager(self, id):

        if id in self.mapper:
            del self.mapper[id]


class ProcessStartController(APIView):

    def get(self, request, id):
        manager = ObjectMapper.get_manager(id, True)

        if manager.get_process_status() == 0:
            return Response("Process already running", 400)

        else:
            resp = manager.start_long_process(id)
            return resp


class ProcessPauseController(APIView):

    def post(self, request, id):
        manager = ObjectMapper.get_manager(id, False)

        if manager is None:
            return Response('Process not running', 400)
        resp = manager.pause_long_process()
        return resp


class ProcessResumeController(APIView):

    def post(self, request, id):
        manager = ObjectMapper.get_manager(id, False)

        if manager is None:
            return Response('Process not running', 400)

        resp = manager.resume_long_process()
        return resp


class ProcessStopController(APIView):

    def post(self, request, id):
        manager = ObjectMapper.get_manager(id, False)

        if manager is None:
            return Response('Process not running', 400)

        resp = manager.cancel_long_process()

        if resp.status_code == 200:
            ObjectMapper.remove_manager(id)

        return resp
