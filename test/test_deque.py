from collections import deque

d = deque([1,2,3], maxlen=3)
d.append(4)
print(d)
d.appendleft(0)
print(d)


d = deque()
d.append(1)
d.append(2)
d.append(3)
print(len(d))
print(d[0])
print(d[-1])

d = deque('12345')
print(len(d))
print(d.popleft())
print(d.pop())
print(d)

d = deque(maxlen=30)
d = deque([1,2,3,4,5])
d.extend([6,7,8])
d.extendleft([0])
print(d)

# deque recipes

def tail(filename, n=5):
    """Return the last n lines of a file"""
    with open(filename) as f:
        return deque(f, n)

# print(tail('1.txt'))
