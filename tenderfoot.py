import random

class Tenderfoot():

	def __init__(self):
		self.INF 	= 1000000
		self.depth 	= 3
		self.ply 	= {}

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

		if depth == 0 or board.find_terminal_state() != ('CONTINUE', '-'):
			return self.heuristic(board)

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

	def heuristic(self, board):
		return (1,(-1,-1))