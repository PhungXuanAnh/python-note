# NOTE: it must set task_default_queue = 'default', in celeryconfig ( default name maybe celery )
# and specify default queue while running worker
# if not the task which is called without specified queue will not be run by any worker

# NOTE: 2: all kinds of pool in celery: 
# prefork
# solo
# eventlet
# gevent
# reference: https://distributedpython.com/posts/celery-execution-pools-what-is-it-all-about/

rm-log-dir:
	rm -rf .celery && rm -rf logs && sleep 1

run-worker-eventlet:
	../.venv/bin/celery worker \
		-A celery_tasks \
		--loglevel=info \
		--concurrency=300 \
		--pool=eventlet \
		-n worker1@%h \
		-Q default,queue1,queue2


run-worker:
	../.venv/bin/celery worker \
		-A celery_tasks \
		--loglevel=info \
		--concurrency=3 \
		-n worker1@%h \
		-Q default,queue1,queue2

run-worker-watchdog:
	../.venv/bin/watchmedo auto-restart --directory . \
		--ignore-pattern='*/call_tasks.py' \
		--pattern '*.py' \
		--recursive \
		-- ../.venv/bin/celery worker \
			-A celery_tasks \
			--loglevel=info \
			--concurrency=3 \
			-n worker1@%h \
			-Q default,queue1,queue2

# ==================================================== routed worker ========================================== 
run-worker-route-feed-media:
	../.venv/bin/celery worker \
		-A celery_tasks \
		--loglevel=info \
		--concurrency=3 \
		-n worker1@%h \
		-Q feed,media


# ============================= worker with priority task ========================================== 
run-worker-normal:
	../.venv/bin/celery worker \
		-A celery_tasks \
		--loglevel=info \
		--concurrency=1 \
		-n worker_normal@%h \
		-Q default,high_priority

run-worker-high-priority:
	../.venv/bin/celery worker \
		-A celery_tasks \
		--loglevel=info \
		--concurrency=1 \
		-n worker-high_priority@%h \
		-Q high_priority

# ==================================================== beat ========================================== 
run-beat:
	celery beat -A celery_tasks --loglevel=info

run-beat-watchdog:
	watchmedo auto-restart --directory . \
		--pattern '*.py' \
		--recursive \
		-- ../.venv/bin/celery beat -A celery_tasks --loglevel=info

test:
	../.venv/bin/python call_tasks.py

remove-result:
	rm -rf .celery/result/*