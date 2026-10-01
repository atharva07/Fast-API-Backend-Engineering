import threading
import time
from app.background.queue import job_queue, acknowledge_job, get_job, redeliver_job, check_visiblity_timeout
from app.background.job import JobStatus, TestExecutionJob

MAX_RETRIES = 3

def process_test_execution(job: TestExecutionJob) -> None:
    worker_name = threading.current_thread().name

    job.status = JobStatus.PROCESSING
    job.attempts += 1

    print(
        f"{worker_name}: Starting Test Execution "
        f"test_case={job.test_case_id}, "
        f"attempt={job.attempts} "
    )

    time.sleep(5)

    if job.attempts == 1:
        raise RuntimeError(
            "Simulated temporary failure"
        )

    job.status = JobStatus.SUCCESS

    print(
        f"{worker_name}: Test Execution Completed "
        f"test_case={job.test_case_id}, "
        f"attempt={job.attempts} "
    )

def worker() -> None:
    worker_name = threading.current_thread().name

    print(f"{worker_name} started")

    while True:
        job = get_job()

        try:
            print(
                f"{worker_name}: Received Job "
                f"test_case={job.test_case_id} "
            )

            process_test_execution(job)

            acknowledge_job(job)

            print(
                f"{worker_name}: ACK "
                f"test_case={job.test_case_id} "
            )

        except Exception as exc:
            print(
                f"{worker_name}: Job Failed "
                f"test_case={job.test_case_id}: {exc} "
            )

            redeliver_job(job)

        finally:
            job_queue.task_done()

def start_workers(
        worker_count: int = 2
) -> list[threading.Thread]:

    threads = []

    for worker_number in range(worker_count):
        thread = threading.Thread(
            target = worker,
            daemon = True,
            name = f"worker-{worker_number + 1} "
        )

        thread.start()
        threads.append(thread)

    return threads

def visibility_monitor() -> None:
    while True:
        check_visiblity_timeout()
        time.sleep(1)

def start_visibility_monitor() -> threading.Thread:

    thread = threading.Thread(
        target=visibility_monitor,
        daemon=True,
        name="visibility-monitor",
    )

    thread.start()

    return thread