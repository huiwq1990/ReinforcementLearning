import heapq

class UniquePriorityQueue(object):
    """ implement the min queue, assuming that each item is unique"""
    def __init__(self, L = []):
        """ initialize the priority queue with some (priority, value) pairs """
        # copy the list values
        self.queue = L[:]
        heapq.heapify(self.queue)
        # initialize the dictionary
        self.dic = {}
        for (p, v) in self.queue:
            self.dic[v] = 1

    def push(self, priority, value):
        heapq.heappush(self.queue, (priority, value))
        self.dic[value] = 1

    def pop(self):
        (priority, value) = heapq.heappop(self.queue)
        del self.dic[value]
        return (priority, value)

    def push_or_update(self, priority, value):
        if not(value in self.dic):
            self.push(priority, value)
        else:
            # if the state is in the queue, update it with the potentially smaller value
            index = 0
            for pair in self.queue:
                (temp, entry) = pair
                if entry == value:
                    self.queue[index] = (min(temp, priority), value)
                    break
                index += 1
            heapq.heapify(self.queue)
            
    def __getitem__(self, index):
        return self.queue[index]
    
    def __contains__(self, value):
        return value in self.dic
    
    def __len__(self):
        return len(self.queue)
        