list1 = [1, 2, 3]
for val in list1:
    print(val)
if isinstance(list1, list):
    print("That is list")

mylist = [0, 1, 2, 3, 4, 5]
#        -6 -5 -4 -3 -2 -1
# chi so duong thi duyet tu phai sang trai, phan tu dau tien co chi 0,  duyet cung chieu kim dong ho
# chi so am thi duyet tu trai sang phai, phan tu dau tieng co chi so -1, duyet nguoc chieu kim dong ho
print('LIST: {}'.format(mylist))
print('phan tu so 0: {}'.format(mylist[0]))
print('phan tu so -1: {}'.format(mylist[-1]))
print('tu phan tu so 3 sang phai: {}'.format(mylist[3:]))
print(
    'tu phan tu so 3 sang trai, khong tinh phan tu so 3: {}'.format(mylist[:3]))
print('tu phan tu so 1 den phan tu so 4, khong tinh phan tu so 4: {}'.format(
    mylist[1:4]))
print(
    'tu phan tu so -5 den phan tu so -2, khong tinh phan tu so -2: {}'.format(mylist[-5:-2]))
# ============================================================
# slices a list
# x[start_at:end_before:step]
# neu step > 0 thi duyet list tu trai sang phai, cung chieu kim dong ho
# neu step < 0 thi duyet list tu phai sang trai, nguoc chieu kim dong ho
# ============================================================
x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
print(x)  # NOTE: python3 using print(list(x))
print('---------chi so duong-------------')
print(x[::1])
print(x[::2])
print(x[3:16:2])
print('---------chi so am-------------')
print(x[::-1])
print(x[::-2])
print(x[-3:-16:-2])

# ==========================================
# chia 1 list thanh cac list nho hon
# split a list into chunks/small lists
# ==========================================


def split_into_chunks(lst, chunk_len):
    try:
        # python 2
        return [lst[x:x + chunk_len] for x in xrange(0, len(lst), chunk_len)]
    except NameError:
        # python 3
        return [lst[x:x + chunk_len] for x in range(0, len(lst), chunk_len)]


print(split_into_chunks(range(0, 50), 10))

# ==========================================
# noi 2 list va bo cac phan tu lap nhau
# combine/join 2 list, then remove duplicated elements, then sort list
# ==========================================


def combine_join_remove_duplicated_and_sort(list1, list2):
    new_lst = list1 + list2     # join 2 list
    # convert list to set to remove duplicated items
    new_set = set(new_lst)
    new_lst = list(new_set)     # convert set to list again
    new_lst = sorted(new_lst)   # sort list
    return new_lst


# return sorted(list(set(list1+list2)))
list1 = [0, 2, 6]
list2 = [9, 1, 3, 6, 7, 2]
print(combine_join_remove_duplicated_and_sort(list1, list2))


list4 = [
    {'a': 123, 'b': 1234},
    {'a': 123, 'b': 1234},
    {'a': 123, 'b': 1234},
    {'a': 3222, 'b': 1234},
]

def remove_duplicate_dict(list_of_dicts):
    # this function to remove duplicate dict from a list of dicts
    print('--------------------------------------------------------------------')
    print('remove DUPLICATE dict in list of dict')
    print('origin list', list_of_dicts)
    # -------------------------------------- method 1
    seen = set()
    new_l = []
    for d in list_of_dicts:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)
    print('method 1: result: ', new_l)
    # -------------------------------------- method 2
    new_d = []
    for x in list_of_dicts:
        if x not in new_d:
            new_d.append(x)
    print('method 2: result: ', new_d)


def duyet_cac_phan_tu_trong_list_theo_chi_so():
    print('--------------------------------------------------------------------')
    print('---------duyet cac phan tu trong list theo chi so-------------')
    t_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for index in range(0, len(t_list) - 1):
        print('phan tu so {} la: {}'.format(index, t_list[index]))

    print('--------------in ra noi dung cua range(5, 0, -1) trong python 3---------------')
    print(list(range(5, 0, -1)))  # print range for python 3

    list1 = [1]
    list2 = [0]
    print(list1 * 3 + list2 * 9)


def remove_None_value_inline_for_loop():
    print('--------------------------------------------------------------------')
    print('remove None value in list')
    test_list = [1, None, 4, None, None, 5, 8, None]
    print ("The original list is : " + str(test_list))
    print ("method 1: List after removal of None values : ",  [i for i in test_list if i])
    print ("method 2: List after removal of None values : ",  list(filter(None, test_list)))


if __name__ == "__main__":
    duyet_cac_phan_tu_trong_list_theo_chi_so()
    remove_duplicate_dict(list4)
    remove_None_value_inline_for_loop()