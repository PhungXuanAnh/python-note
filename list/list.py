list_t=[
                  {"name": "image", "value": "123"},
                  {"name": "flavor", "value": "456"},
                  {"name": "agent_user", "value": "centos"}
        ]
print (list_t[0])
for i,val in enumerate(list_t):
    if(val["name"] == "image"): print (val["value"])
    
for val in list_t:
    print (val)
    
list1 = ['0', '1', '2']

print (list1[2])

if not list1:
    print ("aaa")
    
if isinstance(list1, list):
    print ("That is list")
    
mylist = [0, 1, 2, 3, 4, 5]
'        -6 -5 -4 -3 -2 -1   '
print('phan tu so 1: {}'.format(mylist[1]))
print('phan tu so -1: {}'.format(mylist[-1]))
print('tu phan tu so 3 sang phai: {}'.format(mylist[3:]))
print('tu phan tu so 3 sang trai, khong tinh phan tu so 3: {}'.
    format(mylist[:3]))
print('tu phan tu so 1 den phan tu so 4, khong tinh phan tu so 4: {}'.
    format(mylist[1:4]))
print('tu phan tu so -5 den phan tu so -2, khong tinh phan tu so -2: {}'.
    format(mylist[-5:-2]))
'''
slices a list : cat lat 1 list
x[startAt:endBefore:step]
'''
x = range(20)
print (x)       #NOTE: python3 using print(list(x))
print (x[::1])
print (x[::2])
print(x[3:16:2])
'''
neu step > 0 thi duyet list tu trai sang phai
neu step < 0 thi duyet list tu phai sang trai
'''
print (x[::-1])
print (x[::-2])
print (x[-3:-16:-2])


data = range(0, 103)
# python 2
chunks = [data[x:x+10] for x in xrange(0, len(data), 10)]
# python 3
# chunks = [data[x:x+10] for x in range(0, len(data), 10)]
print(chunks)

# def chunks(l, n):
#     # For item i in a range that is a length of l,
#     # for i in xrange(0, len(l), n):      # python 2
#     for i in range(0, len(l), n):     # python 3
#         # Create an index range for l of n items:
#         yield l[i:i+n]
# # lst = list(chunks[xrange(0, 101), 10])
# lst = list(chunks[range(0, 101), 10])
# print(lst)




