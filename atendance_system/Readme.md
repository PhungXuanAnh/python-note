- [Idea](#idea)
- [Setup environment](#setup-environment)
- [Run main file](#run-main-file)
- [Run test](#run-test)

# Idea

The idea is using key with format **attendance:yyyy-mm-dd** and length 100 to save status of 100 user in a specific day
    1: is present status
    0: is absence status

To set status of user in a specific day using command:
    `redis.setbit(attendance:yyyy-mm-dd, user_id, 1)`

To get status of a user in a specific day using command:
    `redis.getbit(attendance:yyyy-mm-dd, user_id)`

To improve performance of system, we can use lua script for get bit position based on value 1/0

# Setup environment

    - ubuntu 18.08
    - python 3.6.6
    - redis server: host='localhost', port=6379, db=1

Install python package

`pip install -r requirements.txt`

# Run main file

`python attendance_system.py`

# Run test

`python atten_system_unittest.py`
    

