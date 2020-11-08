import time
from threading import Thread
from rest_framework.response import Response


class ProcessManager:

    def __init__(self):
        self.is_running = False
        self.is_paused = False
        self.is_cancelled = False
        super().__init__()

    def start_long_process_thread(self, id):
        from process.controller.process import ObjectMapper
        self.is_running = True
        for i in range(15):

            while self.is_paused:
                time.sleep(2)

            if self.is_cancelled:
                self.revert_changes()
                break

            print("Running long process")
            time.sleep(1)
        ObjectMapper.remove_manager(id)

    def start_long_process(self, id):
        self.thread = Thread(target=self.start_long_process_thread, args=(id,))
        self.thread.start()
        return Response({'Status': 'Process Started'}, 200)

    def pause_long_process(self):

        if self.is_running:
            self.is_running = False
            self.is_paused = True
            return Response({'Status': 'Pause'}, 200)

        else:
            return Response('Process not running', 400)

    def cancel_long_process(self):
        self.is_running = False
        self.is_paused = True
        self.is_cancelled = True
        return Response({'Status': 'Cancelled'}, 200)

    def resume_long_process(self):

        if self.is_paused:
            self.is_running = True
            self.is_paused = False
            return Response({'Status': 'Resumed'}, 200)
        else:
            return Response('Process not paused', 400)

    def revert_changes(self):
        pass

    def get_process_status(self):

        if self.is_running:
            return 0

        elif self.is_cancelled:
            return 1

        elif self.is_paused:
            return 2

        else:
            return -1
