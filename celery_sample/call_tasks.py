# -*- coding: utf-8 -*-
import redis
import uuid
from celery import group, chain, chord
from celery_tasks import (
    longtime_add,
    add,
    print_result,
    chord_task,
    print_result_queue1,
    print_result_queue2,
    test_base_class,
    time_limited,
    MyTask,
    my_task,
    fail_task_retry,
    fail_task,
    forever_task,
    countdown_task,
    wait_for
)
from task_routed_sample.feed.tasks import task_feed
from task_routed_sample.image.tasks import task_image
from task_routed_sample.video.tasks import task_video
from task_routed_sample.web.tasks import task_web

import time
from celery_app import app


def sample_call_a_task():
    # Use one of above lines to call task
    result = add.apply_async([1, 1])
    # result = add.apply_async([1, 1], queue="queue1")

    time.sleep(1)
    print("Task finished? ", result.ready())
    print("Task result 1:   ", result.result)
    print(
        "Task result 2:   ", result.get()
    )  # NOTE: this line will block util get result
    # print_result_queue1.delay("task from queue1")
    # print_result_queue2.delay("task from queue2")


def sample_call_long_task():
    result = longtime_add.apply_async([1, 2], queue="queue2")
    # at this time, our task is not finished, so it will return False
    print("Task finished? ", result.ready())
    print("Task result:   ", result.result)
    # sleep 5 seconds to ensure the task has been finished
    time.sleep(5)
    # now the task should be finished and ready method will return True
    print("Task finished? ", result.ready())
    print("Task result:   ", result.result)


def sample_callback():
    add.apply_async((1, 1), link=print_result.s())


def sample_chains():
    """[
        chains cac task voi nhau (noi voi nhau)
        http://docs.celeryproject.org/en/master/userguide/canvas.html#chains
    ]
    """
    c = chain(add.s(1, 1), add.s(1), add.s(1))
    res = c()
    print(res.get())
    print(res.parent.get())
    print(res.parent.parent.get())


def sample_group():
    """ gọi 1 group các task add """
    g = group(add.s(1, 1), add.s(2, 2), add.s(3, 3))
    resp = g()
    print(resp.get())

    """
    gọi 1 group các task longtime_add và check, đợi kết quả
    tham khảo các hàm khác của group ở đây:
    http://docs.celeryproject.org/en/master/userguide/canvas.html#group-results
    """
    job = group([longtime_add.s(1, 1), longtime_add.s(2, 2), longtime_add.s(3, 3)])
    result = job.apply_async()
    # check result
    print("group ready:       ", result.ready())  # have all subtasks completed?
    print("group successful:  ", result.successful())  # were all subtasks successful?
    print("group complete task: ", result.completed_count())
    # wait 3 * 3 + 2 = 11s for ensure all task done
    time.sleep(11)
    print("group ready:      ", result.ready())  # have all subtasks completed?
    print("group successful: ", result.successful())  # were all subtasks successful?
    print("group complete task: ", result.completed_count())

    print("group result:     ", result.get())
    print("group result:     ", result.join())

    """ hủy bỏ tất cả các task trong group """
    g1 = group(
        [
            longtime_add.s(1, 1),
            longtime_add.s(1, 1),
            longtime_add.s(1, 1),
            longtime_add.s(1, 1),
        ]
    )
    resp = g1()
    print(resp)
    # NOTE: remove or cancel this task
    resp.revoke()


def test_max_concurrency_with_callback():
    callback = print_result
    jobs1 = [
        chord_task.s("111"),
        chord_task.s("222"),
        chord_task.s("333"),
        chord_task.s("444"),
        chord_task.s("555"),
        chord_task.s("666"),
    ]

    jobs2 = [
        chord_task.s("777"),
        chord_task.s("888"),
        chord_task.s("999"),
    ]
    result1 = chord(jobs1, callback.s()).delay()
    result2 = chord(jobs2, callback.s()).apply_async(
        retry=True,
        retry_policy={
            "max_retries": 30,
            "interval_start": 0,
            "interval_step": 0.2,
            "interval_max": 0.2,
        },
    )
    print("result1: {}".format(result1))
    print("result2: {}".format(result2))


def test_connection_to_broker_error(num_retry=0):
    max_retries = 10
    if num_retry > max_retries:
        print("Excceed Max number of retry {} times".format(num_retry))
        return
    callback = print_result
    jobs = [
        chord_task.s("111"),
    ]
    try:
        result2 = chord(jobs, callback.s()).apply_async(
            retry=True,
            retry_policy={
                "max_retries": 30,
                "interval_start": 0,
                "interval_step": 0.2,
                "interval_max": 0.2,
            },
        )
        print("result2: {}".format(result2))
    except redis.exceptions.ConnectionError:
        time.sleep(1)
        print("Connection to broker failed. Try sending task again.")
        num_retry = num_retry + 1
        test_connection_to_broker_error(num_retry)
    except Exception as e:
        print(e.args)


def test_time_limited():
    time_limited.apply_async([31], queue="queue1")


def test_call_class_based_Task():
    my_task.apply_async([10], queue="queue1")

    app.register_task(MyTask()).apply_async([11], queue="queue1")
    app.register_task(MyTask()).apply_async([12], queue="queue2")


def test_call_class_based_Task_in_chord():
    callback = print_result

    jobs = [
        app.register_task(MyTask()).s(7).set(queue="queue2"),
        app.register_task(MyTask()).s(6).set(queue="queue2"),
        app.register_task(MyTask()).s(5).set(queue="queue1"),
        app.register_task(MyTask()).s(4).set(queue="queue1"),
        app.register_task(MyTask()).s(3).set(queue="queue1"),
    ]

    result = chord(
        jobs, callback.s().set(link_error=["super_task.error_callback"])
    ).apply_async([], queue="queue1", interval=3)
    print("result: {}".format(result))

def test_call_fail_task_retry():
    task_id = uuid.uuid4().hex
    result = fail_task_retry.apply_async([task_id, 1], queue="queue1", task_id=task_id)
    
    time.sleep(3)

    # remove task and calling forever_task
    app.control.revoke(task_id=task_id, terminal=True)
    print("Task finished? 1 ", result.ready())
    print("Task result:   2 ", result.result)

    # create new task with same id, it will using old task
    # NOTE: because when revoke task, it is not removed from queue, just be marked as revoked task
    # https://stackoverflow.com/a/44429064/7639845
    result = fail_task_retry.apply_async([task_id, 2], queue="queue1", task_id=task_id)
    print("Task finished? 3 ", result.ready())
    print("Task result:   4 ", result.result)


def test_wait_a_task_by_id():
    """
        Reference here: https://stackoverflow.com/a/47226259
    """
    # Test wait single task
    task_id = uuid.uuid4().hex
    longtime_add.apply_async([1, 1], queue="queue1", task_id=task_id)

    result = wait_for.apply_async([task_id], queue="queue1")
    print("Task finished? ", result.ready())
    print("Task result:   ", result.result)
    print("Task result:   ", result.get())

    # Test wait multiple tasks
    task_ids = []
    for _ in range(3):
        task_id = longtime_add.apply_async([1, 1], queue="queue1").task_id
        task_ids.append(task_id)

    result = wait_for.apply_async([task_ids], queue="queue1")
    print("Task finished? ", result.ready())
    print("Task result:   ", result.result)
    print("Task result:   ", result.get())
    

def get_task_state_by_id():
    # see all exist state here: from celery import states
    task_id = uuid.uuid4().hex
    longtime_add.apply_async([1, 1], queue="queue1", task_id=task_id)
    print(" TTTTTTTTTTTTTT {}".format(app.AsyncResult(task_id).state))
    time.sleep(1)
    print(" TTTTTTTTTTTTTT {}".format(app.AsyncResult(task_id).state))
    print(" TTTTTTTTTTTTTT {}".format(app.AsyncResult(task_id).info)) 
    time.sleep(2)
    print(" TTTTTTTTTTTTTT {}".format(app.AsyncResult(task_id).state))
    print(" TTTTTTTTTTTTTT {}".format(app.AsyncResult(task_id).info))       # this line get meta, set by self.update_state()

    fail_task_id = fail_task.apply_async(queue="queue1").task_id
    time.sleep(1)
    print(" TTTTTTTTTTTTTT {}".format(app.AsyncResult(fail_task_id).state))
    print(" TTTTTTTTTTTTTT {}".format(app.AsyncResult(fail_task_id).info)) 

    # reference: https://stackoverflow.com/a/38267978/7639845
    task_id_or_ids = "unknow_task_id"
    print(" TTTTTTTTTTTTTT {}".format(app.AsyncResult(task_id_or_ids).state))    # NOTE: with unknow task_id state is alway == Pending


def test_route():
    task_feed.delay()
    task_image.delay()
  

if __name__ == "__main__":
    # sample_call_a_task()
    # sample_call_long_task()
    # sample_callback()
    # sample_chains()
    # sample_group()
    # result = test_base_class.delay()
    # print('Task finished? ', result.ready())
    # print('Task result:   ', result.result)
    # test_max_concurrency_with_callback()
    # test_connection_to_broker_error()
    # test_time_limited()
    # test_call_class_based_Task()
    # test_call_class_based_Task_in_chord()
    # test_call_fail_task_retry()
    # test_wait_a_task_by_id()
    # get_task_state_by_id()

    test_route()
