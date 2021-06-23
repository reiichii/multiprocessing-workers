import logging
from logging.handlers import QueueHandler
from multiprocessing import Process, Queue
from typing import List

from libs import logging, settings
from libs.job import create_object
from libs.queue_objects import Queue_objects


def worker_main(log_queue, file_queue, configurer):
    configurer(log_queue)
    while True:
        create_object(file_queue)


def main():
    log_queue = Queue(-1)
    # main logger config
    logger = logging.getLogger()
    logger.addHandler(QueueHandler(log_queue))

    # listener config
    listener = logging.listener_configurer(log_queue)
    listener.start()

    logger.info("start queuing objects")
    file_queue = Queue(-1)
    queuing_objects = Queue_objects(
        settings.TOTAL_USERS,
        settings.HARDLIMIT,
        settings.HARDLIMIT_USERS_PARCENTAGE,
        settings.DEFAULT_LIMIT,
    )
    queuing_objects.queue_objects(file_queue)

    workers: List[Process] = []
    try:
        for _ in range(settings.WORKER_NUM):
            process: Process = Process(
                target=worker_main,
                args=(log_queue, file_queue, logging.worker_configurer),
            )
            process.start()
            workers.append(process)

        for worker in workers:
            worker.join()
    except KeyboardInterrupt:
        logger.info("workers shutdown")
        for worker in workers:
            worker.terminate()
        listener.stop()


if __name__ == "__main__":
    main()
