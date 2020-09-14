# NOTE: it must set task_default_queue = 'default', in celeryconfig ( default name maybe celery )
# and specify default queue while running worker
# if not the task which is called without specified queue will not be run by any worker

rm-log-dir:
	rm -rf .celery && rm -rf logs && sleep 1

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

run-beat:
	celery beat -A celery_tasks --loglevel=info

run-beat-watchdog:
	watchmedo auto-restart --directory . \
		--pattern '*.py' \
		--recursive \
		-- ../.venv/bin/celery beat -A celery_tasks --loglevel=info

test:
	../.venv/bin/python call_tasks.py