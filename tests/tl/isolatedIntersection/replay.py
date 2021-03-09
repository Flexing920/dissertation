import numpy as np
import random

class ReplayBuffer():
    def __init__(self, max_size, min_size, input_shape):
        self._mem_size_max = max_size
        self._mem_size_min = min_size
        self._mem_counter = 0

        self._experiences = []

    # add experince
    def add_experience(self, experience):
        self._experiences[self._mem_counter % self._mem_size_max] = experience
        self._mem_counter += 1


    # helper func: get current experiences size
    def _get_current_size(self):
        return len(self._experiences)

    # experience replay
    def get_experiences(self, n):
        # not enough experiences and no experience replay
        if self._get_current_size() < n:
            return []

        # get all current experiences when not enough for n
        if n > self._get_current_size():
            return random.sample(self._experiences, self._get_current_size())

        # get n random experiences
        else:
            return random.sample(self._experiences, n)
        