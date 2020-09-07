# NOTE: nếu chỉ định queue khi chạy worker thì lúc call task cũng phải chỉ định queue
# nếu không task sẽ không chạy 

run-worker:
	../.venv/bin/celery worker \
		-A tasks_sample \
		--loglevel=info \
		--concurrency=3 \
		-n worker1@%h \
		-Q queue1,queue2

run-worker-watchdog:
	../.venv/bin/watchmedo auto-restart --directory . \
		--ignore-pattern='*/call_tasks.py' \
		--pattern '*.py' \
		--recursive \
		-- ../.venv/bin/celery worker \
			-A tasks_sample \
			--loglevel=info \
			--concurrency=3 \
			-n worker1@%h \
			-Q queue1,queue2

run-beat:
	celery beat -A tasks_sample --loglevel=info

run-beat-watchdog:
	watchmedo auto-restart --directory . \
		--pattern '*.py' \
		--recursive \
		-- ../.venv/bin/celery beat -A tasks_sample --loglevel=info

call-task:
	../.venv/bin/python call_tasks.py