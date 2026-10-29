from collections import deque

# generate examples
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_pylist(head):
    result = []
    while head is not None:
        result.append(head.val)
        head = head.next
    return result


def build_cyclic_list(values, pos):

    head = build_list(values)
    if pos < 0 or head is None:
        return head
    target = None
    cur = head
    i = 0
    while cur.next is not None:
        if i == pos:
            target = cur
        cur = cur.next
        i += 1
    if i == pos:
        target = cur
    cur.next = target
    return head


# if linked list has a cycle

def has_cycle(head):
    if head is None or head.next is None:
        return False

    slow = head
    fast = head.next

    while slow is not fast:
        if fast is None or fast.next is None:
            return False
        slow = slow.next
        fast = fast.next.next
    return True

#example
# 11 -> 3 -> 8 -> 9 -> 6 -> 11 -> 16 -> 17 -> back to 8
ll1 = build_cyclic_list([11, 3, 8, 9, 6, 11, 16, 17], 2)
print('has cycle (11->3->8->9->6->11->16->17->8):', has_cycle(ll1))
ll2 = build_list([11, 3, 8, 9, 6, 11, 16, 17])
print('list:', to_pylist(ll2))
print('has cycle:', has_cycle(ll2))

#reverse linked list

def reverse_linked_list(head):
    prev = None
    current = head

    while current is not None:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt

    head = prev
    return head

ll3 = build_list([1, 2, 3, 4])
print('no reversed:', to_pylist(ll3))
print('reversed:', to_pylist(reverse_linked_list(ll3)))


#find middle node of linked list

def middle_node(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow

ll4 = build_list([3, 8, 9, 6, 11, 16, 17])
print('list:', to_pylist(ll4))
print('middle node:', middle_node(ll4).val)


#remove elements from linked list

def remove_elements(head, val):
    dummy = ListNode()
    dummy.next = head
    prev = dummy
    cur = head

    while cur is not None:
        if cur.val == val:
            prev.next = cur.next
        else:
            prev = cur
        cur = cur.next

    return dummy.next

val = 3
ll5 = build_list([1, 2, 3, 4])
print('before removing:', to_pylist(ll5))
print('removed val =', val, ':', to_pylist(remove_elements(ll5, val)))
val = 1
ll6 = build_list([1, 2, 3, 4])
print('before removing:', to_pylist(ll6))
print('removed first, val =', val, ':', to_pylist(remove_elements(ll6, val)))

#remove nth node from end of linked list

def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    slow = dummy
    fast = dummy

    for _ in range(n + 1):
        fast = fast.next

    while fast is not None:
        slow = slow.next
        fast = fast.next

    slow.next = slow.next.next
    return dummy.next

n = 2
ll7 = build_list([1, 2, 3, 4, 5])
print('before removing:', to_pylist(ll7))
print('removed', n, 'node from end:', to_pylist(remove_nth_from_end(ll7, n)))


#is sequence is origin of another sequence
# 6.1  with allocation O(n)

def is_subsequence_queue(a, b):
    q = deque()
    for el in a:
        q.append(el)

    for el in b:
        if q and q[0] == el:
            q.popleft()

    return len(q) == 0

s1, s2 = 'abd', 'uabqd'
print('is subsequence (queue):', s1, s2, is_subsequence_queue(s1, s2))
s3, s4 = 'ooo', 'abcd'
print('is subsequence (queue):', s3, s4, is_subsequence_queue(s3, s4))


#6.2 two pointers, O(1) space

def is_subsequence_two_pointers(a, b):
    i, j = 0, 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1
        j += 1
    return i == len(a)

s5, s6 = 'abd', 'abcd'
print('is subsequence (two pointers):', s5, s6, is_subsequence_two_pointers(s5, s6))
print('is subsequence (two pointers):', s3, s4, is_subsequence_two_pointers(s3, s4))


# 6.3 naive O(n^2)

def is_subsequence_naive(a, b):
    i = 0
    len_a = len(a)
    len_b = len(b)
    for el1 in range(len_a):
        for el2 in range(len_b):
            if a[el1] == b[el2]:
                i += 1
                break
    return i == len_a

print('is subsequence (naive):', s1, s2, is_subsequence_naive(s1, s2))
print('is subsequence (naive):', s3, s4, is_subsequence_naive(s3, s4))

#if the word is a palindrome

# 7.1 stack

def is_palindrome_stack(s):
    stack = []
    for char in s:
        stack.append(char)

    for char in s:
        if char != stack.pop():
            return False
    return True

w1 = 'abcba'
w2 = 'abca'
print('is palindrome (stack):', w1, is_palindrome_stack(w1))
print('is palindrome (stack):', w2, is_palindrome_stack(w2))


# 7.2 deque

def is_palindrome_deque(s):
    d = deque(s)
    while len(d) > 1:
        if d.popleft() != d.pop():
            return False
    return True

print('is palindrome (deque):', w1, is_palindrome_deque(w1))
print('is palindrome (deque):', w2, is_palindrome_deque(w2))


# 7.3 2 pointers

def is_palindrome_two_pointers(s):
    left = 0
    right = len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

print('is palindrome (two pointers):', w1, is_palindrome_two_pointers(w1))
print('is palindrome (two pointers):', w2, is_palindrome_two_pointers(w2))


# 8. Sort a stack using an additional stack

def sort_stack(input_stack):
    stack = []  # дополнительный стек
    while len(input_stack) > 0:
        current = input_stack.pop()
        # перекладываем из доп. стека обратно во входной все элементы,
        # которые больше current
        while len(stack) > 0 and stack[-1] > current:
            input_stack.append(stack.pop())
        stack.append(current)
    return stack

st1 = [2, 3, 1, 4]  # top of the stack is the end of the list
print('no sorted stack:', st1)
print('sorted stack:', sort_stack(st1))

#merge two sorted linked lists

def merge_two_lists(list1, list2):
    dummy = ListNode()
    tail = dummy

    while list1 is not None and list2 is not None:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next

    tail.next = list1 if list1 is not None else list2
    return dummy.next

ll8 = build_list([3, 6, 8])
ll9 = build_list([4, 7, 9, 11])
print('list1:', to_pylist(ll8))
print('list2:', to_pylist(ll9))
print('merged sorted lists:', to_pylist(merge_two_lists(ll8, ll9)))
