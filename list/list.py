list_t=[
                  {"name": "image", "value": "123"},
                  {"name": "flavor", "value": "456"},
                  {"name": "agent_user", "value": "centos"}
        ]
print list_t[0]
for i,val in enumerate(list_t):
    if(val["name"] == "image"): print val["value"]
    
for val in list_t:
    print val
    
list1 = ['0', '1', '2']

print list1[2]

if not list1:
    print "aaa"
    
if isinstance(list1, list):
    print "That is list"
    
mylist = []
mylist.append("asdf")
mylist.append("jkl;")
print mylist[0][0] 
print mylist[0][1:]
print mylist[0][:1]


