import copy
from functools import total_ordering
from hw8_lib import Stack
from hw8_lib import BinarySearchTree


class ByteNode:
    """
    this class represents an 8 characters long byte with a pointer for the next byte
    """
    def __init__(self, byte):
        """
        the builder function for the 'ByteNode' class
        :param byte: Object, 8 characters long which contains only 1's and 0's
        """
        try:  # if byte is wrong type it wont be able to iterate in the next line
            if not all(x == '0' or x == '1' for x in byte):  # checks the content in 'byte'
                raise ValueError("byte must contain only '1' or '0'")
        except TypeError:
            raise TypeError(f"{type(byte)} is wrong type for a byte")
        if len(byte) != 8:  # check the length
            raise ValueError(f"byte must be 8 characters long but got {len(byte)}")
        self.byte = byte
        self.next = None

    def get_byte(self):
        """
        a function which retrieves the data of the node
        :return: str, the data of the node
        """
        return str(self.byte)

    def get_next(self):
        """
        a function which retrieves the next node
        :return: None/NodeByte , the next byte
        """
        return self.next

    def set_next(self, next):
        """
        a function that updates the next byte
        :param next: ByteNode, the desired next byte
        """
        self.next = next

    def __repr__(self):
        """
        a function which overrides the repr method for ByteNode
        :return: str, the representation of the ByteNode object
        """
        return f'[{str(self.byte)}]=>'


@total_ordering
class LinkedListBinaryNum:
    """
    a class which represents a binary number using ByteNodes and linked list
    """
    def __init__(self, num=0):
        """
        the constructor for the class it turns a decimal number to binary number represented by bytes and linked list
        :param num: num, the decimal number
        """
        if not isinstance(num, int):  # check to see if got a decimal num
            raise TypeError(f"Expected int but got {type(num)}")
        if num < 0:  # working with positive numbers only
            raise ValueError("Only positive numbers please")
        binary_num = ''
        node_binary_num = None
        size = 1
        while num != 0:  # this loop divides the number until it is 0 and adds the remainder to the binary num
            if len(binary_num) == 8:  # turns the binary num to a byte
                size += 1
                msb = ByteNode(binary_num)
                msb.set_next(node_binary_num)
                node_binary_num = msb
                binary_num = ''
            digit = num % 2
            num = num // 2
            binary_num = str(digit) + binary_num
        while len(binary_num) != 8:  # adds zero to the num until i can turn it to a byte
            binary_num = '0' + binary_num
        msb = ByteNode(binary_num)
        msb.set_next(node_binary_num)
        node_binary_num = msb
        self.size = size
        self.head = node_binary_num

    def add_MSB(self, byte):
        """
        this function adds a byte to the head of the linked list
        :param byte: str, binary number 8 chars long
        :return: None
        """
        bn = ByteNode(byte)
        bn.set_next(self.head)
        self.head = bn
        self.size += 1

    def __len__(self):
        """
        overrides the len method for this class
        :return: int, the length of the linked list
        """
        return copy.deepcopy(self.size)

    def __str__(self):#end user
        """
        overrides the str representation for linked list
        :return: str, the representation of the binary number
        """
        b_num = '|'
        b_node = self.head
        while b_node:
            b_num = b_num + b_node.get_byte() + '|'
            b_node = b_node.get_next()  # runs thought all the bytes in the list
        return b_num

    def __repr__(self):#developer
        """
        overrides the developers representation for linked list
        :return: str, the developers representation for linked list
        """
        b_node = self.head
        print_b_node = ''
        while b_node:
            print_b_node = print_b_node + b_node.__repr__()  # uses the representation of the byte node
            b_node = b_node.get_next()
        print_b_node = print_b_node + 'None'
        plural = ''
        if self.size > 1:  # adds 's' to 'byte' if needed
            plural = 's'
        return f'LinkedListBinaryNum with {self.size} Byte{plural}, Bytes map: {print_b_node}'

    def __getitem__(self, item):
        """
        overrides the getitem method for the linked list
        :param item: int, the position of the desired item
        :return: str, the byte in the desired position
        """
        if not isinstance(item, int):  # item must be int
            raise TypeError(f"expected int but received {type(item)}")
        if item >= self.size or (item + 1) * -1 >= self.size:  # check if the desired position is valid
            raise IndexError("Wrong index habibi")
        b_node = self.head
        if item == 0:
            return b_node.get_byte()
        elif item > 0:  # loop for positive index
            for byte in range(item):
                b_node = b_node.get_next()
        else:  # loop for negative index
            while item*-1 < self.size:
                b_node = b_node.get_next()
                item -= 1
        return b_node.get_byte()

    def __eq__(self, other):
        """
        overrides the '==' operator for the linked list
        :param other: int/LinkedListBinaryNum, what to compare the current linked list with
        :return:  boolean , True if both equal False if not
        """
        if isinstance(other, int):  # turn int into a LinkedListBinaryNum
            other = LinkedListBinaryNum(other)
        if not isinstance(other, LinkedListBinaryNum):
            raise TypeError(f"cannot compare LinkedListBinary with{type(other)}")
        if len(other) != self.size:
            return False
        for idx in range(self.size):  # compares each byte in the linked list
            if self[idx] != other[idx]:
                return False
        return True

    def __gt__(self, other):
        if isinstance(other, int):  # turn the other to LinkedListBinaryNum
            other = LinkedListBinaryNum(other)
        if not isinstance(other, LinkedListBinaryNum):
            raise TypeError(f"cannot compare LinkedListBinary with{type(other)}")
        if len(other) == self.size:  # check both only if they got the same length
            for idx in range(self.size):  # compares each byte with the other
                if self[idx] > other[idx]:
                    return True
                elif self[idx] < other[idx]:
                    return False
            return False
        else:
            return self.size > len(other)  # with self is longer then it is also bigger

    def __add__(self, other):
        """
        overrides the '+' operator for LinkedListBinaryNum
        :param other: int/LinkedListBinaryNum, what to add to the number
        :return: LinkedListBinaryNum, the binary representation of the sum of the numbers
        """
        if isinstance(other, int):  # only adds positive numbers
            if other < 0:
                raise ValueError("Only positive numbers please")
            other = LinkedListBinaryNum(other)
        if not isinstance(other, LinkedListBinaryNum):
            raise TypeError(f"cannot add {type(other)} to LinkedListBinary")
        carry = 0
        check = True  # a checker for the first Byte
        sum_all = LinkedListBinaryNum()  # add the sum here
        bin1 = self
        bin2 = other
        sub_len = len(bin1) - len(bin2)
        if sub_len < 0:
            sub_len = sub_len * -1
            bin2 = self
            bin1 = other
        while sub_len > 0:  # a loop that adds zero's so both number have the same length
            sub_len -= 1
            bin2.add_MSB('00000000')
        for idx in range(len(other)-1, -1, -1):  # a loop that does all the adding from the end to start
            result = ''
            for num in range(7, -1, -1):  # a loop that does the adding for a single byte
                r = carry
                if bin1[idx][num] == '1':
                    r += 1
                if bin2[idx][num] == '1':
                    r += 1
                if r % 2 == 1:
                    result = '1' + result
                else:
                    result = '0' + result
                if r < 2:
                    carry = 0
                else:
                    carry = 1
            if sum_all == LinkedListBinaryNum() and check:
                sum_all.head = ByteNode(result)
                check = False
            else:
                sum_all.add_MSB(result)
        if carry != 0:  # if a carry left then another byte needed
            sum_all.add_MSB("00000001")
        return sum_all

    def __sub__(self, other):
        """
        overrides the '-' operator for LinkedListBinaryNum
        :param other: int/LinkedListBinaryNum, the number to subtract
        :return: LinkedListBinaryNum, the subtracted binary number
        """
        if isinstance(other, int):
            if other < 0:  # can only subtract positive numbers
                raise ValueError("Only positive numbers please")
            other = LinkedListBinaryNum(other)
        if not isinstance(other, LinkedListBinaryNum):
            raise TypeError(f"cannot subtract {type(other)} from LinkedListBinary")
        if other > self:
            raise ValueError(f"{self} - {other} will be negative, i dont know how to do this")
        while self.size - len(other) > 0:  # a loop that adds zero's until both have the same length
            other.add_MSB('00000000')
        carry = 0
        check = True
        sub = LinkedListBinaryNum()
        for idx in range(min(self.size, len(other)) - 1, -1, -1):  # a loop that does the whole subtraction
            result = ''
            for num in range(7, -1, -1):  # a loop that subtracts each byte
                if carry == 0:  # split the subtraction for 2 options ,with or without carry
                    if self[idx][num] == other[idx][num]:
                        result = '0' + result
                    elif other[idx][num] == '1':
                        carry += 1
                        result = '1' + result
                    else:
                        result = '1' + result
                else:
                    if self[idx][num] == other[idx][num]:
                        result = '1' + result
                    else:
                        carry = 0
                        result = '0' + result
            if sub == LinkedListBinaryNum() and check:
                sub.head = ByteNode(result)
                check = False
            else:
                sub.add_MSB(result)
        if len(sub) > 1 and sub[0] == '00000000':  # throw away all the 'zero bytes' from the answer
            short_sub = LinkedListBinaryNum()
            short_sub.head = ByteNode(sub[-1])
            for i in range(len(sub)-2, -2, -1):
                if sub[i] == '00000000':
                    break
                short_sub.add_MSB(sub[i])
            return short_sub
        return sub

    def __radd__(self, other):
        """
        a function that overrides the right add operator fot this class
        :param other: int/LinkedListBinaryNum, the number to add to self
        :return: LinkedListBinaryNum, the sum of both numbers
        """
        if isinstance(other, int):
            other = LinkedListBinaryNum(other)
        return other + self


class DoublyLinkedNode:
    """
    this class represents a node that linked back and forth
    """
    def __init__(self, data):
        """
        the constructor for DoublyLinkedNode
        :param data: object, any desired object
        """
        self.data = data
        self.next = None
        self.prev = None

    def get_data(self):
        """
        a function which retrieves the data from the node
        :return: object, the data in the node
        """
        return copy.deepcopy(self.data)

    def set_next(self, next):
        """
        a function which updates the next node for the current node
        :param next: None/DoublyLinkedNode, the node to update
        :return: None
        """
        if not next:
            self.next = next
            return
        self.next = next
        next.prev = self

    def get_next(self):
        """
        retrieves the next node
        :return: None/DoublyLinkedNode, the next node
        """
        return self.next

    def get_prev(self):
        """
        retrieves the previous node
        :return: None/DoublyLinkedNode, the previous node
        """
        return self.prev

    def set_prev(self, prev):
        """
        a function which updates the next node for the current node
        :param prev: None/DoublyLinkedNode, the node to update
        :return: None
        """
        if not prev:
            self.prev = prev
            return
        self.prev = prev
        prev.next = self

    def __repr__(self):
        """
        overrides the developers representation for DoublyLinkedNode
        :return: str , the developers representation
        """
        return f"=>[{str(self.get_data())}]<="


class DoublyLinkedList:
    """
    this class is an abstract data type, doubly linked list
    """
    def __init__(self):
        """
        the constructor for the list, creates an empty list
        """
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        """
        overrides the saved 'len' method
        :return: int, the length of the doubly linked list
        """
        return copy.deepcopy(self.size)

    def add_at_start(self, data):
        """
        a function which adds a node of received data to the first index of the list
        :param data: object, the data to add to the list
        :return: None
        """
        data = DoublyLinkedNode(data)  # turn the data to a node
        if not self.head:
            self.head = data
            self.tail = data
        else:
            data.set_next(self.head)
            self.head.set_prev(data)
            self.head = data
        self.size += 1

    def remove_from_end(self):
        """
        a function which removes the item at the last index of the list
        :return: object, the data from the removed node
        """
        if not self.tail:
            return None
        new_tail = self.tail.get_prev()
        old_tail = self.tail
        if self.size > 1:
            new_tail.set_next(None)
        self.tail = new_tail
        self.size -= 1
        return old_tail.get_data()

    def get_tail(self):
        """
        a function which retrieves the node at the last index of the list
        :return: DoublyLinkedNode, the node at the last index
        """
        return copy.deepcopy(self.tail)

    def get_head(self):
        """
        a function which retrieves the node at the first index of the list
        :return: DoublyLinkedNode, the node at the first index
        """
        return copy.deepcopy(self.head)

    def __repr__(self):
        """
        overrides the developers representation for DoublyLinkedList
        :return: str , the developers representation of the list
        """
        if self.size == 0:
            return "Head==><==Tail"
        the_print = "Head="
        data_node = self.head
        while data_node:  # loop that runs thought the list and adds the data of all the nodes as str
            the_print = the_print + str(data_node)
            data_node = data_node.get_next()
        return the_print + "=Tail"

    def is_empty(self):
        """
        function that checks if the list is empty
        :return: boolean, True if the list is empty false if not
        """
        return self.size == 0


class DoublyLinkedListQueue:
    """
    a claas that represents an abstract data type 'queue' uses the method FIFO
    """
    def __init__(self):
        """
        the constructor of the queue
        """
        self.data = DoublyLinkedList()

    def enqueue(self, val):
        """
        a function that adds an item to the queue to the end of the queue
        :param val: object, the object to add to the queue
        :return: None
        """
        self.data.add_at_start(val)

    def dequeue(self):
        """
        a method that removes an item from the queue using FIFO
        :return: object, the object at the start of the queue
        """
        if not self.data:
            raise StopIteration("No more queue 4 U")
        return self.data.remove_from_end()

    def __len__(self):
        """
        a function which retrieves the length of the queue
        :return: int, the length of the queue
        """
        return len(self.data)

    def is_empty(self):
        """
        a function which checks if the queue is empty
        :return: boolean, True if the queue is empty
        """
        return len(self.data) == 0

    def __repr__(self):
        """
        overrides the developers representation for DoublyLinkedNode
        :return: str , the developers representation of the queue
        """
        start = "Newest=>["
        end = "]<=Oldest"
        if self.is_empty():
            return start + end
        for i in range(len(self)):  # a loop that runs through all the items in the queue
            runner = self.dequeue()
            end = ','+str(runner) + end
            self.enqueue(runner)
        return start + end[1:]

    def __iter__(self):
        """
        override of the iter operator for the queue
        :return: DoublyLinkedListQueue, the copy of the queue
        """
        return copy.deepcopy(self)

    def __next__(self):
        """
        override of the next function for DoublyLinkedListQueue
        :return:
        """
        temp = self.dequeue()
        return temp


class NumsManagment:
    """
    a class which help analyze data from a file
    """
    def __init__(self, file_name):
        """
        the constructor of the class
        :param file_name: str, any type of text file
        """
        self.file_name = file_name

    def is_line_pos_int(self, st):
        """
        a function which check if a line from text file is a natural number
        :param st: str, a line from a text file
        :return: boolean, True if st is a natural number, False if not
        """
        try:
            st = int(st[:-1])  # if not a whole number it raises an exception
        except ValueError:
            return False
        return st >= 0

    def read_file_gen(self):
        """
        a function which returns a generator that retrieves all the natural numbers in a file
        :return: generator, all the natural numbers as a binary numbers
        """
        with open(self.file_name, 'r') as f:
            for line in f:
                if self.is_line_pos_int(line):  # returns the number only if it is natural
                    yield LinkedListBinaryNum(int(line[:-1]))

    def stack_from_file(self):
        """
        a function which creates a stack of all the natural numbers and stores them as binary numbers
        :return: Stack , contains natural numbers in the file as binary numbers
        """
        stack = Stack()
        try:
            gen = self.read_file_gen()
            line = next(gen)
        except FileNotFoundError or StopIteration:  # stop the code from failing if there are no numbers in the file
            return stack
        while line:  # a loop that runs through all the numbers in the file
            stack.push(line)
            try:
                line = next(gen)
            except StopIteration:
                return stack

    def sort_stack_descending(self, s):
        """
        a function which reorders the stack in a descending order
        :param s: Stack, contains binary numbers
        :return: Stack , reordered stack
        """
        order_s = Stack()
        spare_s = Stack()
        while not s.is_empty():  # a loop that checks all the numbers in the given stack
            num = s.pop()
            if order_s.is_empty() or num >= order_s.top():
                order_s.push(num)
            else:
                while not order_s.is_empty():  # a loop that puts the number in the right place
                    if num < order_s.top():
                        spare_s.push(order_s.pop())
                    else:
                        break
                order_s.push(num)
                while not spare_s.is_empty():  # a loop that returns all the numbers back to the ordered stack
                    order_s.push(spare_s.pop())
        return order_s

    def queue_from_file(self):
        """
        a function which creates a queue of all the natural numbers and stores them as binary numbers
        :return:  DoublyLinkedListQueue, contains natural numbers in the file as binary numbers
        """
        queue = DoublyLinkedListQueue()
        try:
            gen = self.read_file_gen()
            line = next(gen)
        except FileNotFoundError or StopIteration:  # stop the code from failing if there are no numbers in the file
            return queue
        while line:  # a loop that runs through all the numbers in the file and adds them to the queue
            queue.enqueue(line)
            try:
                line = next(gen)
            except StopIteration:
                return queue

    def set_of_bytes(self, q_of_nums):
        """
        a function which turns a queue of binary numbers to a set of the numbers
        :param q_of_nums: DoublyLinkedListQueue, a queue of natural binary numbers
        :return: set, the binary numbers that was in the queue without duplicates
        """
        nums_set = set()
        for num in q_of_nums:  # a loop that adds al the numbers to the set
            for i in range(len(num)):
                nums_set.add(str(num[i]))
        return nums_set

    def nums_bst(self):
        """
        a function which creates a binary search tree of all the natural numbers and stores them as binary numbers
        :return:  BinarySearchTree, contains natural numbers in the file as binary numbers
        """
        bst = BinarySearchTree()
        with open(self.file_name, 'r') as f:
            for line in f:  # adds all the natural numbers to the tree
                if self.is_line_pos_int(line):
                    num = int(line[:-1])
                    bst.insert(num, LinkedListBinaryNum(num))
        return bst

    def bst_closest_gen(self, bst):
        """
        a function which finds 2 numbers that are closest to each other in a BinarySearchTree and generates all the
        numbers between them, including the numbers themselves
        :param bst: BinarySearchTree, a tree data type with binary numbers
        :return: generator, that generates all the numbers between the closest numbers in the tree
        """
        min_range = 0
        num = bst.__iter__()
        num = next(num)
        min_num = num
        for next_num in bst:  # a loop that checks all the numbers in the tree
            if min_range == 0:  # creates the first true distance
                min_range = next_num[0]-num[0]
            elif next_num[0]-num[0] < min_range:  # a condition which grantees to have the closest 2 numbers
                min_num = num
                min_range = next_num[0]-num[0]
            num = next_num
        for i in range(min_range+1):  # a loop of the generator itself
            yield min_num[0]+i, min_num[1]+i
