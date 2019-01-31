watchmedo auto-restart --directory . \
                        --pattern '*.py' \
                        --recursive \
                        -- celery worker -A tasks_sample --loglevel=info