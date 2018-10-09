Redis is an in-memory datastructure server. It has facility to manipulate
bitstrings in their Strings datastructure. There are 100 users. Some of them
come to the office, some are absent on any particular day. Everyday they
come, they log-in to an attendance system. We have to know how many users
logged-in on a particular day. Please use Redis Bitstrings to find a solution and
code it (Python or GO) so that in real time we can query how many users (out
of 100) have logged in till now and print their ids.
We are also interested in knowing all the users who came on consecutive days
and those who were absent on two consecutive days. Please write the code
and test cases so that you generate 100 users attendance randomly on both
days and print out
- the total counts of presence each day (along with their ids)
- the total count of absence each day (along with their ids)
- the total count of users who were present on two consecutive days (along
with their ids)
- the total count of users who were absent on two consecutive days (along
with their ids)
