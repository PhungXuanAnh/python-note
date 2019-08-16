watchmedo auto-restart --directory . \
                        --pattern '*.py' \
                        --recursive \
                        -- celery worker \
                            -A tasks_sample \
                            --loglevel=info \
                            --concurrency=6 \
                            -n worker1@%h \
                            -Q queue1,queue2
