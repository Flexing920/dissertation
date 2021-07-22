from collections import deque
import numpy as np

class ReplayBuffer():

    def __init__(self, maxlen):
        self.buffer = deque(maxlen=maxlen)
        self.priorities = deque(maxlen=maxlen)
    
    def add(self, experience):
        self.buffer.append(experience)
        self.priorities.append(max(self.priorities, default=1))

    def get_probability(self, priority_scale):
        scaled_priorities = np.array(self.priorities) ** priority_scale
        sample_priorities = scaled_priorities / sum(scaled_priorities)
        return sample_priorities

    def get_importance(self, probabilities):
        importance = 1/len(self.buffer) * 1/probabilities
        importance_normalized = importance / max(importance)
        return importance_normalized

    def sample(self, batch_size, priority_scale=1.0):
        if len(self.buffer) >= batch_size:
            sample_probs = self.get_probability(priority_scale)
            sample_indices = random.choices(range(len(self.buffer)), k=batch_size, weights=sample_probs)
            samples = np.array(self.buffer)[sample_indices]
            importance = self.get_importance(sample_probs[sample_indices])
            return map(list, zip(*samples)), importance
        return