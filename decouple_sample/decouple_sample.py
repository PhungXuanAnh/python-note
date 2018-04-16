from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
PERCENTILE = config('PERCENTILE', default='50%')

print(SECRET_KEY)
print(DEBUG)
print(EMAIL_HOST)
print(EMAIL_PORT)
print(PERCENTILE)
