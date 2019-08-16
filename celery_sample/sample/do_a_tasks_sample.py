from celery import group, chain, chord
from tasks_sample import longtime_add, add, print_result, chord_task,\
    print_result_queue1, print_result_queue2
import time


def sample_call_a_task():
    result = add.apply_async([1, 1], queue='queue1')
    time.sleep(1)
    print('Task finished? ', result.ready())
    print('Task result:   ', result.result)
    print_result_queue1.delay('task from queue1')
    print_result_queue2.delay('task from queue2')


def sample_call_long_task():
    result = longtime_add.delay(1, 2)
    # at this time, our task is not finished, so it will return False
    print('Task finished? ', result.ready())
    print('Task result:   ', result.result)
    # sleep 5 seconds to ensure the task has been finished
    time.sleep(5)
    # now the task should be finished and ready method will return True
    print('Task finished? ', result.ready())
    print('Task result:   ', result.result)


def sample_callback():
    add.apply_async((1, 1), link=print_result.s())


def sample_chains():
    """[
        chains cac task voi nhau (nối với nhau)
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
    print('group ready:       ', result.ready())         # have all subtasks completed?
    print('group successful:  ', result.successful())    # were all subtasks successful?
    print('group complete task: ', result.completed_count())
    # wait 3 * 3 + 2 = 11s for ensure all task done
    time.sleep(11)
    print('group ready:      ', result.ready())         # have all subtasks completed?
    print('group successful: ', result.successful())    # were all subtasks successful?
    print('group complete task: ', result.completed_count())

    print('group result:     ', result.get())
    print('group result:     ', result.join())

    """ hủy bỏ tất cả các task trong group """
    g1 = group([longtime_add.s(1, 1), longtime_add.s(1, 1), longtime_add.s(1, 1), longtime_add.s(1, 1)])
    resp = g1()
    print(resp)
    resp.revoke()


def test_max_concurrency_with_callback():
    jobs = [
        chord_task.s('111111111'),
        chord_task.s('222222222'),
        chord_task.s('333333333'),
        chord_task.s('444444444'),
        chord_task.s('555555555'),
        chord_task.s('666666666'),
    ]

    jobs1 = [
        chord_task.s('777777777'),
        chord_task.s('888888888'),
        chord_task.s('999999999'),
    ]
    result = chord(jobs1, print_result.s()).delay()
    result = chord(jobs, print_result.s()).delay()
    # result = chord(jobs, print_result.s()).delay()


if __name__ == '__main__':
    # sample_call_a_task()
    # sample_call_long_task()
    # sample_callback()
    # sample_chains()
    # sample_group()

    test_max_concurrency_with_callback()
