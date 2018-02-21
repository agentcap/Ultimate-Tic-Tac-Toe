import random

class Tenderfoot():

	def __init__(self):
		self.INF 	= 1000000
		self.depth 	= 4
		self.ply 	= {}

	def move(self, board, old_move, flag):
	
		if flag == "x":			
			self.ply["max"]	= "x"
			self.ply["min"] = "o"
		else:
			self.ply["max"] = "o"
			self.ply["min"] = "x"

		score = self.minimax(board, self.depth, -self.INF, self.INF, old_move, True)

		return score[1]


	def minimax(self, board, depth, alpha, beta, old_move, is_max_ply):

		if depth == 0 or board.find_terminal_state()[0] != "CONTINUE":
			return self.heuristic(board)

		moves = board.find_valid_move_cells(old_move)

		if is_max_ply:
			max_score = -self.INF
			max_moves = []
			for mv in moves:
				board.update(old_move, mv, self.ply["max"])
				
				score = self.minimax(board,depth-1,alpha,beta,mv,False)[0]
				if(max_score < score):
					max_score = score
					max_moves = [mv]
				elif max_score == score:
					max_moves.append(mv)
				
				board.block_status[mv[0]/4][mv[1]/4]= '-'
				board.board_status[mv[0]][mv[1]] 	= '-'
				
			return (max_score, random.choice(max_moves))

		else:
			min_score = self.INF
			min_moves = []
			for mv in moves:
				board.update(old_move, mv, self.ply["min"])
				
				score = self.minimax(board,depth-1,alpha,beta,mv,True)[0]
				if(min_score > score):
					min_score = score
					min_moves = [mv]
				elif min_score == score:
					min_moves.append(mv)
				
				board.block_status[mv[0]/4][mv[1]/4]= '-'
				board.board_status[mv[0]][mv[1]] 	= '-'
				
			return (min_score, random.choice(min_moves))

	def heuristic(self, board):
		return (1,(-1,-1))