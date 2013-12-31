import unittest
from PriorityQueue import UniquePriorityQueue

class UniquePriorityQueueTest(unittest.TestCase):
    def setup(self):
        pass
    
    def test_1(self):
        queue = UniquePriorityQueue()
        queue.push(2, 3)
        queue.push(0, 5)
        queue.push(8, 1)
        (p, v) = queue.pop()
        self.assertEqual(5, v)        
        (p, v) = queue.pop()
        self.assertEqual(3, v)        
        (p, v) = queue.pop()
        self.assertEqual(1, v)  
    
    def test_2(self):
        queue = UniquePriorityQueue()
        queue.push_or_update(2, 3)
        queue.push_or_update(10, 5)
        queue.push_or_update(8, 1)
        queue.push_or_update(0, 5)
        queue.push_or_update(4, 6)
        (p, v) = queue.pop()
        self.assertEqual(5, v)        
        (p, v) = queue.pop()
        self.assertEqual(3, v)        
        (p, v) = queue.pop()
        self.assertEqual(6, v)  
        (p, v) = queue.pop()
        self.assertEqual(1, v)          
        queue.push_or_update(10, 5)
        (p, v) = queue.pop()
        self.assertEqual(5, v)          
    
if __name__ == '__main__':
    unittest.main()