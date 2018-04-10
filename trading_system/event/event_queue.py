import queue

from .event import Event


class EventQueue:
    """
    Container for the event queue object.
    """

    def __init__(self):
        self._event_queue = queue.Queue()

    def get_next_event(self):
        try:
            event = self._event_queue.get_nowait()
        except queue.Empty:
            raise EmptyQueueException
        return event

    def add_event(self, event: Event):
        self._event_queue.put(event)


class EmptyQueueException(queue.Empty):
    pass
