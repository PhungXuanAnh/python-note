'''
Viet code va testcase tao ra 100 nguoi dung lien tiep vang mat hoac lien tiep co mat va in ra

- tong so nguoi co mat moi ngay va id
- tong so nguoi vang mat moi ngay va id
- tong so nguoi dung co mat 2 ngay lien tiep va id
- tong so nguoi dung mat mat 2 ngay lien tiep va id

model:
- user_id - not null
- date login - not null
- time login - maybe null
- status: present/absent - not null

user_id: {
    date:
    time:
    status:
}

user_id = [0, ..., 99]
date:  [user_id, user_id, user_id ]
'''

import random


def genarate_user():
    '''
    - tao 100 nguoi dung ngau nhien co mat hoac vang mat lien tiep 2 ngay
    - tao trong 30 ngay
    '''
    counts_present = random.randint(0, 100)
    list_id_present = random.sample(range(0, 99), counts_present)

    for i in range(1, 30):
        write_database(i: list_id_present)


list_present_consecutive_day = []
list_absent_consecutive_day = []

list_id_present_tmp = []
list_id_absent_tmp = []
for i in range(1, 30):
    list_id_present = get_date(i)

    # in ra tong so nguoi co mat hang ngay va id
    print(len(list_id_present), list_id_present)

    list_id_absent = list(range(0, 99))
    for id in list_id_present:
        list_id_absent.remove(id)

    # in ra tong so nguoi vang mat hang ngay va id
    print(len(list_id_absent), list_absent)

    for id in list_id_present_tmp:
        if id in list_id_present:
            list_present_consecutive_day.append(id)

    for id in list_id_absent_tmp:
        if id in list_id_absent:
            list_absent_consecutive_day.append(id)

    list_id_present_tmp = list_id_present
    list_id_absent_tmp = list_id_absent


list_present_consecutive_day = list(set(list_present_consecutive_day))
list_absent_consecutive_day = list(set(list_absent_consecutive_day))

print(len(list_present_consecutive_day), list_present_consecutive_day)
print(len(list_absent_consecutive_day), list_absent_consecutive_day)
