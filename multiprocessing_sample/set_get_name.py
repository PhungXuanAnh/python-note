import multiprocessing
import time


def worker():
    name = multiprocessing.current_process().name
    print(name, 'Starting')
    time.sleep(3)
    print(name, 'Exiting')


def my_service():
    name = multiprocessing.current_process().name
    print(name, 'Starting')
    time.sleep(5)
    print(name, 'Exiting')


if __name__ == '__main__':
    service = multiprocessing.Process(name='my_service', target=my_service)
    worker_1 = multiprocessing.Process(name='worker 1', target=worker)
    worker_2 = multiprocessing.Process(name='worker 2', target=worker)
    default = multiprocessing.Process(target=worker)  # use default name

    worker_1.start()
    worker_2.start()
    service.start()
    default.start()

    print(worker_1.is_alive(),
    worker_2.is_alive(),
    service.is_alive(),
    default.is_alive()
    )
    worker_1.terminate()
    worker_2.terminate()
    service.terminate()
    default.terminate()

