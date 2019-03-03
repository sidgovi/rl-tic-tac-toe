import numpy as np
import random

qtable = np.zeros([2,3**9,9])
board = {}

def init_board():
	for i in range(0, 9):
		board[i] = ' '
def print_board():
	print(board[0], board[1], board[2])
	print(board[3], board[4], board[5])
	print(board[6], board[7], board[8])

def avail_moves():
	l = []
	for i in range(0, 9):
		if board[i] == ' ':
			l.append(i)
	return l

def is_winner():
	l = [[0,1,2],[3,4,5],[6,7,8],[0,4,8],[2,4,6],[0,3,6],[1,4,7],[2,5,8]]
	for ll in l:
		if board[ll[0]] != ' ' and board[ll[0]] == board[ll[1]] and board[ll[1]] == board[ll[2]]:
			return board[ll[0]]
	return False

def is_full():
	for i in range(0, 9):
		if board[i] == ' ':
			return False

	return True

def is_done():
	if is_winner() or is_full():
		return True
	return False

def reward(player):
	if not is_winner():
		return 0

	if (is_winner() == player):
		return 1

	return -1

def place_move(player, square):
	if board[square] != ' ':
		return True
	board[square] = player
	return False


def get_random_move():
	l = avail_moves()
	r = random.randint(1, len(l))
	return l[r-1]


def get_curr_best_move(state, player):
	if player == 'X':
		val= 0
	else:
		val= 1

	return np.argmax(qtable[val, state])

def get_state():
	state = 0
	for i in range(0,9):
		if board[i] == ' ':
			val = 0
		elif board[i] == 'X':
			val = 1
		elif board[i] == 'O':
			val = 2

		state += val * (3**(8-i))
	return state
	
def agent(player):
	state = 0
	move = 0
	epsilon = .1
	alpha = .1
	gamma = .6
	index =0
	move_count = 0
	#print("player=",player)
	while not is_done():
		if player == 'X':
			index = 0
			opp_player = 'O'
		else:
			index = 1
			opp_player = 'X'
		if random.uniform(0,1) < epsilon:
			move = get_random_move()
			place_move(player, move)
		else:
			state = get_state()
			move = get_curr_best_move(state, player)
			illegal =  place_move(player, move)
			if illegal:
				continue

		agent_opp(opp_player)
	#	raw_input("Press enter to continue")
		old_val = qtable[index,state, move]
		next_state = get_state()
		next_max = np.max(qtable[index, next_state])
		rew = reward(player)
	#	print("player=",player,"reward =", rew)
		new_val = (1 - alpha) * old_val + alpha * (rew + gamma * next_max)
		qtable[index,state,move] = new_val

def agent_opp(player):
	epsilon = .1
	if player == 'X':
		index = 0
		opp_player = 'O'
	else:
		index = 1
		opp_player = 'X'

#	print("player = ",player)
#	print_board()
#	print("-------")
	illegal = True
	if not is_done(): 
		while illegal == True:
#			if random.uniform(0,1) < epsilon:
#				move = get_random_move()
#				place_move(player, move)
#				illegal = False
#			else:
			state = get_state()
			move = get_curr_best_move(state, player)
			illegal =  place_move(player, move)
#		print_board()
#		print("-------")
	else:
		return False
	
	return True

def play():
	init_board()
	while not is_done():
		move = input("Move?")
		place_move('X', move)
		print_board()
		print qtable[1,get_state()]
		move = get_curr_best_move(get_state(), 'O')
		place_move('O', move)
		print_board()
		
nepoch = 500000
for i in range (0, nepoch):
	init_board()
	if i % 2 == 0:
		player = 'X'
		agent(player)
	else:
		agent_opp('X')
		player = 'O'
		agent(player)
	if i % 1000 == 0:
		print i, "/", nepoch

np.save("qtable-500k", qtable)
#qtable = np.load("qtable.npy")
#play()
