import queue


class EventQueue:
    """
    Container for the event queue object.
    """

    def __init__(self):
        self._event_queue = queue.Queue()

    def maybe_get_next_event(self):
        """If there is another event in the queue, return it, else return None."""
        try:
            return self._event_queue.get_nowait()
        except queue.Empty:
            return None

    def add_event(self, event):
        self._event_queue.put(event)
