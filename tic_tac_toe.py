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
	
def train_agentx(nepoch):
	state = 0
	move = 0
	epsilon = .1
	alpha = .5
	gamma = .6
	index =0
	move_count = 0
	player = ' '
	for i in range(0, nepoch):
		if i % 1000 == 0:
			print i, "/", nepoch
		init_board()
		move_count = 0
		while not is_done():
			if move_count % 2 == 0:
				player = 'X'
				index = 0
			else:
				player = 'O'
				index = 1
			if random.uniform(0,1) < epsilon:
				move = get_random_move()
				place_move(player, move)
			else:
				state = get_state()
				move = get_curr_best_move(state, player)
				illegal =  place_move(player, move)
				if illegal:
					continue
			move_count += 1
			old_val = qtable[index,state, move]
			next_state = get_state()
			next_max = np.max(qtable[index, next_state])
			rew = reward(player)
			new_val = (1 - alpha) * old_val + alpha * (rew + gamma * next_max)
			qtable[index,state,move] = new_val

def play():
	init_board()
	while not is_done():
		print qtable[0,get_state()]
		move = get_curr_best_move(get_state(), 'X')
		place_move('X', move)
		print_board()
		move = input("Move?")
		place_move('O', move)
		print_board()
		
		

train(10000000)
play()


print qtable[0,0]
