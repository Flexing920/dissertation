import os
from pathlib import Path
from collections import namedtuple
import random
import tensorflow as tf
# experience = namedtuple("Experience", 
#     field_names=["state", "action", "reward", "next_state", "done"])

# from collections import deque
# samples = deque(maxlen=5)
# samples.append(([1,2,3,4], 1, [1,1,1,1], 5))
# samples.append(([2,3,4,5], 2, [2,1,1,1], 10))
# samples.append(([3,3,3,3], 1, [2,2,2,2], 2))

# # print(samples)

# s = random.choices(samples, k=2,weights=[1,2,3])
# print(s)

# a = map(list, zip(*s))
# print(list(a))
import time
time_stamp = ''.join(str(time.time()).split('.'))
print(time_stamp)