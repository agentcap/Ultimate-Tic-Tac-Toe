import random

class Tenderfoot():

	def __init__(self):
		self.INF 	= 1000000
		self.depth 	= 3
		self.ply 	= {}
		self.block_weights = [[6, 4, 4, 6], [4, 3, 3, 4], [4, 3, 3, 4], [6, 4, 4, 6]]
		self.winning_comb = []
		for i in range(4):
			comb = []
			for j in range(4):
				comb.append((i, j))
			self.winning_comb.append(comb)

		for j in range(4):
			comb = []
			for i in range(4):
				comb.append((i, j))
			self.winning_comb.append(comb)

		comb = [(1, 2), (2, 1), (2, 3), (3, 2)]
		self.winning_comb.append(comb)
		comb = [(1, 1), (2, 0), (2, 2), (3, 1)]
		self.winning_comb.append(comb)
		comb = [(0, 2), (1, 1), (1, 3), (2, 2)]
		self.winning_comb.append(comb)
		comb = [(0, 1), (1, 0), (1, 2), (2, 1)]
		self.winning_comb.append(comb)

	def move(self, board, old_move, flag):
	
		if flag == "x":			
			self.ply["max"]	= "x"
			self.ply["min"] = "o"
		else:
			self.ply["max"] = "o"
			self.ply["min"] = "x"

		score,move = self.minimax(board, self.depth, -self.INF, self.INF, old_move, True)

		return move


	def minimax(self, board, depth, alpha, beta, old_move, is_max_ply):

		terminal_status = board.find_terminal_state()
		if depth == 0 or terminal_status != ('CONTINUE', '-'):
			if terminal_status[1] == 'WON':
				if terminal_status[0] == self.ply["max"]:
					return (10, old_move)
				else:
					return (-10, old_move)
			boardmax = self.heuristic(board, self.ply["max"])
			boardmin = self.heuristic(board, self.ply["min"])
			for i in range(4):
				for j in range(4):
					if boardmax[i][j] == 1:
						boardmin[i][j] = 0
					if boardmin[i][j] == 1:
						boardmax[i][j] = 0

			return (self.find_prob_block(boardmax) - self.find_prob_block(boardmin), old_move)


		moves = board.find_valid_move_cells(old_move)

		if is_max_ply:
			max_score = -self.INF
			max_move  = (-1,-1)
			for mv in moves:
				board.update(old_move, mv, self.ply["max"])
				
				score = self.minimax(board, depth-1, alpha, beta, mv, False)[0]

				board.block_status[mv[0]/4][mv[1]/4]= '-'
				board.board_status[mv[0]][mv[1]] 	= '-'

				alpha = max(alpha,score)
				if(max_score < score):
					max_score = score
					max_move = mv
				if(alpha >= beta):
					break
				
			return (max_score, max_move)

		else:
			min_score = self.INF
			min_move = (-1,-1)
			for mv in moves:
				board.update(old_move, mv, self.ply["min"])
				
				score = self.minimax(board,depth-1,alpha,beta,mv,True)[0]

				board.block_status[mv[0]/4][mv[1]/4]= '-'
				board.board_status[mv[0]][mv[1]] 	= '-'

				beta = min(beta,score)
				if(min_score > score):
					min_score = score
					min_move  = mv
				if(alpha >= beta):
					break
				
			return (min_score, min_move)

	def heuristic(self, board, flag):
		# return (1,(-1,-1))
		board_prob = [[0 for i in range(4)] for j in range(4)]
		for i in range(4):
			for j in range(4):
				if board.block_status[i][j] == '-': 
					board_prob[i][j] = self.find_prob_cells(board.board_status, 4*i, 4*j, flag)
				elif board.block_status[i][j] == flag:
					board_prob[i][j] = 1

		# return self.find_prob_block(board_prob)
		return board_prob

	def find_prob_cells(self, board_status, topx, topy, flag):

		total_prob = 0
		for comb in self.winning_comb:
			prob = 1
			for (x, y) in comb:
				if board_status[topx + x][topy + y] == '-':
					prob *= 0.5
				elif board_status[topx + x][topy + y] != flag:
					prob *= 0
			if prob == 1:
				return 1
			total_prob += prob

		return total_prob / 12

	def find_prob_block(self, board_prob):

		total_prob = 0
		for comb in self.winning_comb:
			prob = 1
			for (x, y) in comb:
				prob *= board_prob[x][y]
			if prob == 1:
				return 1
			total_prob += prob

		return total_prob / 12