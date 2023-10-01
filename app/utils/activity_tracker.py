import datetime
from threading import Lock

class LastActivityTracker:
    def __init__(self):
        self.last_activity_times = {}
        self.lock = Lock()

    def update_activity_time(self, session_id):
        with self.lock:
            self.last_activity_times[session_id] = datetime.datetime.now()

    def remove_activity_time(self, session_id):
        with self.lock:
            if session_id in self.last_activity_times:
                del self.last_activity_times[session_id]

    def get_inactive_sessions(self, timeout):
        with self.lock:
            inactive_sessions = []
            now = datetime.datetime.now()
            for session_id, last_activity_time in self.last_activity_times.items():
                if (now - last_activity_time).total_seconds() > timeout:
                    inactive_sessions.append(session_id)
            return inactive_sessions
