s1 = "key1: {} \\ \n"\
    "\tkey2: {} \\ \n"\
    "\tkey3: {}".format('value1', 'value2', 'value3')

print(s1)

# https://stackoverflow.com/a/10660477/7639845
account_id = "account_123"
def_id = "123123"
query = ('SELECT   action.descr as "action", '
         'role.id as role_id,'
         'role.descr as role'
         ' FROM '
         'public.role_action_def,'
         'public.role,'
         'public.record_def, '
         'public.action'
         ' WHERE role.id = role_action_def.role_id AND'
         ' record_def.id = role_action_def.def_id AND'
         ' action.id = role_action_def.action_id AND'
         ' role_action_def.account_id = '+account_id+' AND'
         ' record_def.account_id='+account_id+' AND'
         ' def_id='+def_id)
print(query)

print("\n\n\n This line will \
get carried over to\
 the new line.\
Notice how this\
word will be together because \
of no space around it")
