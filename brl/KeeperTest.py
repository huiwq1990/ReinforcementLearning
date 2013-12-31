import unittest
from RLKeeper import *
from ChainModel import *

class KeeperTest(unittest.TestCase):

    def setUp(self):
        self.keepr = Keeper()
        self.model = ChainModel()
        self.act_a = self.model.act_a
        self.act_b = self.model.act_b
        self.s1 = self.model.get_state_by_id(1)
        self.s2 = self.model.get_state_by_id(2)
        self.s3 = self.model.get_state_by_id(3)
    
    def test_sums(self):
        self.keepr.update_reward_sums(self.s1, self.act_a, 2)
        self.keepr.update_reward_sums(self.s1, self.act_a, 10)
        self.keepr.update_reward_sums(self.s2, self.act_b, 8)
        self.keepr.update_reward_sums(self.s2, self.act_b, 7)
        self.assertEqual(self.keepr.get_sum_reward(self.s1, self.act_a), 12) 
        self.assertEqual(self.keepr.get_sum_reward(self.s2, self.act_b), 15)
        self.assertEqual(self.keepr.get_sum_reward(self.s1, self.act_b), 0)
        self.assertEqual(self.keepr.get_sum_reward_squares(self.s1, self.act_a), 104)
        self.assertEqual(self.keepr.get_sum_reward_squares(self.s2, self.act_b), 113)
        self.assertEqual(self.keepr.get_sum_reward_squares(self.s1, self.act_b), 0)
    
    def test_reward_model(self):
        self.keepr.update_reward_and_transition(self.s1, self.act_a, self.s2, 2)
        self.keepr.update_reward_and_transition(self.s1, self.act_a, self.s2, 3)
        self.keepr.update_reward_and_transition(self.s2, self.act_b, self.s2, 1)
        self.assertEqual(self.keepr.get_reward(self.s1, self.act_a, self.s2), 2.5, "This")
        self.assertEqual(self.keepr.get_reward(self.s2, self.act_b, self.s2), 1.0)
        self.assertEqual(self.keepr.get_reward(self.s1, self.act_a, self.s3), 0)
        self.keepr.update_reward_and_transition(self.s1, self.act_a, self.s3, 1)
        self.assertEqual(2.0/3, self.keepr.get_var_reward(self.s1, self.act_a))
        self.keepr.update_reward_and_transition(self.s1, self.act_a, self.s3, 1)
        self.assertEqual(0.6875, self.keepr.get_var_reward(self.s1, self.act_a))
    
    def test_transition_model(self):
        self.keepr.update_transition(self.s1, self.act_a, self.s2)
        self.keepr.update_transition(self.s1, self.act_a, self.s2)
        self.keepr.update_transition(self.s1, self.act_a, self.s3)
        self.keepr.update_transition(self.s1, self.act_b, self.s2)
        self.assertEqual(self.keepr.get_visit_count(self.s1), 4)
        self.assertEqual(self.keepr.get_visit_count(self.s1, self.act_a), 3)
        self.assertEqual(self.keepr.get_visit_count(self.s1, self.act_b), 1)
        self.assertEqual(self.keepr.get_transition(self.s1, self.act_a, self.s2), 2.0/3)
        self.assertEqual(self.keepr.get_transition(self.s1, self.act_a, self.s3), 1.0/3)
        self.assertEqual(self.keepr.get_transition(self.s1, self.act_b, self.s2), 1.0)
        self.assertEqual(self.keepr.get_transition(self.s1, self.act_b, self.s3), 0)

if __name__ == '__main__':
    unittest.main()