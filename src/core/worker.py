import threading
import queue
import concurrent.futures
import multiprocessing

class ParallelWorker:
    """A worker that can execute tasks in parallel using a thread pool."""
    def __init__(self, max_workers=None):
        if max_workers is None:
            # Use number of CPU cores, but at least 2
            max_workers = max(2, multiprocessing.cpu_count())
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.futures = []

    def submit(self, func, *args, **kwargs):
        """Submit a task to the worker."""
        future = self.executor.submit(func, *args, **kwargs)
        self.futures.append(future)
        return future

    def shutdown(self, wait=True):
        """Shutdown the executor."""
        self.executor.shutdown(wait=wait)

class SerialWorker(threading.Thread):
    """A traditional serial worker for tasks that must be done in order."""
    def __init__(self, error_callback=None):
        super().__init__(daemon=True)
        self.q = queue.Queue()
        self._stop_event = threading.Event()
        self.error_callback = error_callback

    def run(self):
        while not self._stop_event.is_set():
            try:
                job = self.q.get(timeout=0.2)
                if job is None:
                    break
                func, args, kwargs = job
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    if self.error_callback:
                        self.error_callback(e)
                finally:
                    self.q.task_done()
            except queue.Empty:
                continue

    def submit(self, func, *args, **kwargs):
        self.q.put((func, args, kwargs))

    def stop(self):
        self._stop_event.set()
        self.q.put(None)
