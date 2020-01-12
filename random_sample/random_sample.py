import random

print('choose 1 random number in range 0 - 9: ', random.randint(0, 9))


foo = ['a', 'b', 'c', 'd', 'e']
print('random choice from a specified list: ', random.choice(foo))
foo = [1, 2, 0, 0, 3, 4, 8, 9]
print('random choice from a specified list: ', random.choice(foo))

# choose a random child list from a larger list
print(random.sample(range(0, 10), 3))
print(random.sample(range(0, 10), 3))
print(random.sample(range(0, 10), 4))
print(random.sample(range(0, 10), 5))
