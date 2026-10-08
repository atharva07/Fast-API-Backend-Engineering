from queue import Queue
from threading import Lock
import time
from app.background.job import TestExecutionJob

job_queue = Queue()

in_flight_jobs: dict[int, tuple[TestExecutionJob, float]] = {}

in_flight_lock = Lock()

VISIBILITY_TIMEOUT = 10

def get_job() -> TestExecutionJob:
    job = job_queue.get()

    with in_flight_lock:
        in_flight_jobs[id(job)] = (
            job,
            time.time()
        )

    return job

def acknowledge_job(job: TestExecutionJob) -> None:
    with in_flight_lock:
        in_flight_jobs.pop(
            id(job),
            None
        )

def redeliver_job(job: TestExecutionJob) -> None:
    with in_flight_lock:
        in_flight_jobs.pop(
            id(job),
            None
        )

    job.status = "PENDING"

    job_queue.put(job)

def check_visiblity_timeout() -> None:
    now = time.time()

    expired_jobs = []

    with in_flight_lock:
        for job_id, (job, delivered_at) in in_flight_jobs.items():
            elapsed = now - delivered_at

            if elapsed >= VISIBILITY_TIMEOUT:
                expired_jobs.append(job_id)

        for job_id in expired_jobs:
            with in_flight_lock:
                item = in_flight_jobs.pop(job_id, None)

            if item is not None:
                job, _ = item

                print(
                    f"Visibility timeout expired "
                    f"for test_case={job.test_case_id}"
                )

                job.status = "PENDING"

                job_queue.put(job)