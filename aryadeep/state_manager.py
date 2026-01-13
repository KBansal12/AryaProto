import threading

class StateManager:
    def __init__(self):
        self._interrupt_event = threading.Event()
        self._current_operation = None
        self._lock = threading.Lock()
    
    def set_current_operation(self, operation_name):
        with self._lock:
            self._current_operation = operation_name
            self._interrupt_event.clear()
    
    def clear_current_operation(self):  
        with self._lock:
            self._current_operation = None
    
    def get_current_operation(self):
        with self._lock:
            return self._current_operation
    
    def request_interrupt(self):
        with self._lock:
            if self._current_operation:
                self._interrupt_event.set()
                return True
            return False
    
    def should_interrupt(self):
        return self._interrupt_event.is_set()
    
    def wait_if_not_interrupted(self, timeout=None):
        return not self._interrupt_event.wait(timeout=timeout)

# Global state manager instance
state_manager = StateManager()