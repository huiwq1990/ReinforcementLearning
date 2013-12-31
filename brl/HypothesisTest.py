import unittest
from Hypothesis import Hypothesis
from RLKeeper import Keeper
from ChainModel import *

class HypothesisTest(unittest.TestCase):
    def setUp(self):
        self.model = ChainModel()
        self.act_a = self.model.act_a
        self.act_b = self.model.act_b
        self.s1 = self.model.get_state_by_id(1)
        self.s2 = self.model.get_state_by_id(2)
        self.s3 = self.model.get_state_by_id(3)
    
    def test_init_hypothesis(self):
        u0 = 1
        std0 = 1
        hypothesis = Hypothesis.draw_init_hypothesis(self.model, u0, std0)
        self.assertEqual((u0, std0), hypothesis.get_reward_table(self.s1, self.act_a))
        self.assertEqual((u0, std0), hypothesis.get_reward_table(self.s1, self.act_b))
        self.assertEqual((u0, std0), hypothesis.get_reward_table(self.s1, self.act_a))
        self.assertEqual((u0, std0), hypothesis.get_reward_table(self.s2, self.act_b))
        self.assertEqual((u0, std0), hypothesis.get_reward_table(self.s2, self.act_a))
        self.assertEqual((u0, std0), hypothesis.get_reward_table(self.s3, self.act_b))
        self.assertEqual((u0, std0), hypothesis.get_reward_table(self.s3, self.act_a))
        next_states = self.model.get_next_states(self.s1)
        s = 0
        for next_state in next_states:
            p = hypothesis.get_transition(self.s1, self.act_a, next_state)
            s += p
            self.assertGreater(p, 0)
        self.assertAlmostEqual(s, 1)

    def test_draw_hypothesis(self):
        keepr = Keeper()
        for i in range(1000):
            keepr.update_reward_and_transition(self.s1, self.act_a, self.s2, 1.4)        
        hypothesis = Hypothesis.draw_hypothesis(self.model, keepr)
        for next_state in self.model.get_next_states(self.s1):
            self.assertGreater(hypothesis.get_transition(self.s1, self.act_a, next_state), 0)
        places = 1
        self.assertAlmostEqual(hypothesis.get_transition(self.s1, self.act_a, self.s2), 1, places)       
        self.assertAlmostEqual(hypothesis.get_reward(self.s1, self.act_a), 1.4, places)            
        
if __name__ == '__main__':
    unittest.main()