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
'''slices a list : cat lat 1 list
x[startAt:endBefore:step]'''
x = range(20)
print (x)
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

print([] + "abc")

