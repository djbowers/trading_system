import queue


class EventQueue:
    """
    Container for the event queue object.
    """

    def __init__(self):
        self._event_queue = queue.Queue()

    def get_next_event(self):
        return self._event_queue.get_nowait()

    def add_event(self, event):
        self._event_queue.put(event)
