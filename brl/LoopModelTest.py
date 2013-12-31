from LoopModel import *

def test_loop_a():
	model = LoopModel()
	(state0, state1, state2, state3, state4) = model.get_states_by_id([0, 1, 2, 3, 4])
	assert model.current_state == state0
	reward = model.perform_action_a()
	assert model.current_state == state1
	assert reward == 0
	reward = model.perform_action_a()
	assert model.current_state == state2
	assert reward == 0
	reward = model.perform_action_a()
	assert model.current_state == state3
	assert reward == 0
	reward = model.perform_action_a()
	assert model.current_state == state4
	assert reward == 0	
	reward = model.perform_action_a()
	assert model.current_state == state0
	assert reward == 1

def test_loop_b():
	model = LoopModel()
	(state0, state5, state6, state7, state8) = model.get_states_by_id([0, 5, 6, 7, 8])
	assert model.current_state == state0
	reward = model.perform_action_b()
	assert model.current_state == state5
	assert reward == 0
	reward = model.perform_action_b()
	assert model.current_state == state6
	assert reward == 0
	reward = model.perform_action_b()
	assert model.current_state == state7
	assert reward == 0
	reward = model.perform_action_b()
	assert model.current_state == state8
	assert reward == 0
	reward = model.perform_action_a()
	assert model.current_state == state0
	assert reward == 2

def test_transition_6_0():
	model = LoopModel()
	(state0, state6) = model.get_states_by_id([0, 6])
	model.set_current_state_by_state_id(6)
	reward = model.perform_action_a()
	assert model.current_state == state0
	assert reward == 0

test_loop_a()
test_loop_b()
test_transition_6_0()