watchmedo auto-restart --directory . \
                        --pattern '*.py' \
                        --recursive \
                        -- celery beat -A tasks_sample --loglevel=info