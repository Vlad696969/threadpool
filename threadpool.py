import threading
from queue import Queue
import requests


class ThreadPool:
    """
    Simple implementation of a thread pool that takes a list of tasks and waits for all tasks to execute
    Attributes:
        _run_event (threading.Event): flag indicating that the threads should start pulling from the task queue
        _size (int): number of threads in the pool
        _queue (queue.Queue): task queue
        _pool (list): list of threads
        _destroyed (bool): flag indicating that the thread pool has been destroyed
    """
    def __init__(self, size=1):
        self._run_event = threading.Event()  # Used to indicate when the threads should start pulling from the queue
        self._size = size  #
        self._queue = Queue()
        self._pool = []
        self._destroyed = False

        # Create the thread pool
        for i in range(self._size):
            thread = threading.Thread(target=self._worker)
            self._pool.append(thread)
            thread.daemon = True  # Ensure that threads are destroyed when the main thread is finished
            thread.start()

    def _worker(self):
        # Worker will run until thread pool is terminated
        while True:
            if self._destroyed:
                break

            # Wait until threadpool is started
            self._run_event.wait()

            task = self._queue.get()  # Blocking
            task.execute()
            self._queue.task_done()  # Signal that task has been finished

    def submit(self, tasks):
        """
        Give a list of tasks to the thread pool and wait for its execution
        :param tasks: list of tasks
        """
        if self._destroyed:
            raise Exception('Unable to add task the pool has already been destroyed.')
        for task in tasks:
            self._queue.put(task)
        self._run_event.set()  # Allow the threads to pull from the queue
        self._queue.join()  # Wait for all task completion
        self._run_event.clear()  # Indicate that the threads should wait again

    def destroy(self):
        if self._destroyed:
            raise Exception('Cannot destroy as the thread pool has already been destroyed.')

        # Flag causes threads to stop pulling from queue and return
        self._destroyed = True


class Task:
    """
    Read the content from an image url and write it locally
    """
    def __init__(self, name, file_url):
        self.name = name
        self.file_url = file_url

    def execute(self):
        file_name = self.file_url.split('/')[-2]
        r = requests.get(self.file_url, allow_redirects=True)
        fp = open(file_name + '.jpg', 'wb')
        fp.write(r.content)
        fp.close()
        print(f'Task {self.name}: file {file_name} downloaded')
