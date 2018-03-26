from queue import Queue


class EventQueue(Queue):
    def get_next_event(self):
        return self.get_nowait()
