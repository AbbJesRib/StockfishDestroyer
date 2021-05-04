import random
import copy

list = [[random.randint(0, 8) for j in range(8)] for i in range(8)]
list1 = list.copy()
list2 = copy.deepcopy(list)
print(list)
print(list.copy())
print(copy.deepcopy(list))

list[6][2] = 100

print(list)
print(list1)
print(list2)