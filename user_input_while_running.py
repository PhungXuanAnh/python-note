'''
Created on Mar 10, 2017

@author: xuananh
'''
# Start with an empty list. You can 'seed' the list with
#  some predefined values if you like.
names = []

# Set new_name to something other than 'quit'.
new_name = ''

# Start a loop that will run until the user enters 'quit'.
while new_name != 'quit':
    # Ask the user for a name.
    new_name = raw_input("Please tell me someone I should know, or enter 'quit': ")

    print (new_name)
    # Add the new name to our list.
    if new_name != 'quit':
        names.append(new_name)

# Show that the name has been added to the list.
print(names)