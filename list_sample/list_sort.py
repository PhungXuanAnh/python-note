list_to_be_sorted = [
    {'name':'ddd', 'age':39}, 
    {'name':'aaa', 'age':10}, 
    {'name':'bbb', 'age':20}, 
    {'name':'ccc', 'age':40},
]

 # reference: https://stackoverflow.com/a/73050/7639845
print(sorted(list_to_be_sorted, key=lambda k: k['age']))   
print(type(sorted(list_to_be_sorted, key=lambda k: k['age'])))

