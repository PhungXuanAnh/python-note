class Node(object):

    def __init__(self, data):
        self.data = data
        self.next_node = None


class Singly_Linked_List(object):

    def __init__(self, node):
        self.head = node

    def print_linked_list(self):
        print_node = self.head

        while print_node is not None:
            print(print_node.data)
            print_node = print_node.next_node

    def insert_begining(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        new_node.next_node = self.head
        self.head = new_node

    def insert_end(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        end_node = self.head
        while end_node.next_node is not None:
            end_node = end_node.next_node

        end_node.next_node = new_node

    def insert_middle(self, data, middle_node):
        new_node = Node(data)

        # kiem tra co middle node khong
        # gan next node cua new node cho next node cua middle node
        # gan next node cua middle node cho new node

        if middle_node is None:
            print('middle node data is absent')
            return

        new_node.next_node = middle_node.next_node
        middle_node.next_node = new_node

    def remove_node(self, data_removed_node):
        # kiem tra node head co phai node remove khong, neu co thi gan node head bang node ket tiep va return
        # neu khong thi gan va duyet tim removed node va previous node
        # gan next node cua previous node cua removed node  cho next node cua removed node
        # gan removed node = None

        if self.head.data == data_removed_node:
            self.head = self.head.next_node
            return

        previous_node = self.head
        current_node = self.head.next_node

        while current_node is not None:
            if current_node.data == data_removed_node:
                previous_node.next_node = current_node.next_node
                current_node = None
                return

            previous_node = current_node
            current_node = current_node.next_node


node1 = Node('Mon')
node2 = Node('Tue')
node3 = Node('Wed')

linked_list = Singly_Linked_List(node1)
linked_list.head.next_node = node2
linked_list.print_linked_list()
print('-------------------------------')

linked_list.insert_begining('Sun')
linked_list.print_linked_list()
print('------------------------------- insert begin')

linked_list.insert_end('Thu')
linked_list.print_linked_list()
print('------------------------------- insert end')

linked_list.insert_middle('Fri', linked_list.head.next_node)
linked_list.print_linked_list()
print('------------------------------- insert middle after node: {}'.format(linked_list.head.next_node.data))

linked_list.remove_node('Sun')
linked_list.print_linked_list()
