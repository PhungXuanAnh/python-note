def sort_list_of_dict():
    list_to_be_sorted = [
        {'name':'ddd', 'age':39}, 
        {'name':'aaa', 'age':10}, 
        {'name':'bbb', 'age':20}, 
        {'name':'ccc', 'age':40},
    ]

    # reference: https://stackoverflow.com/a/73050/7639845
    print(sorted(list_to_be_sorted, key=lambda k: k['age']))   
    print(type(sorted(list_to_be_sorted, key=lambda k: k['age'])))

def sort_list_alphabet():
    cars = ['Ford', 'BMW', 'Volvo']
    cars.sort()
    print(cars)
    list1 = ['x', 'y', 'a', 'b', 'c', 'g', 'h', 'i']
    list1.sort()
    print(list1)
    
if __name__ == '__main__':
    sort_list_alphabet()
    sort_list_of_dict()