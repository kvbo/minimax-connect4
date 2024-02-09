import math
import copy
import time


class Controller:
	def __init__(self, *args, **kwargs):
		self.game = kwargs["game"]
		self.name = kwargs["name"]

	def move(self):
		self.game.print()

	def __str__(self):
		return f"{self.name}"


class HumanController(Controller):
	def move(self):
		super().move()

		column = input(f"{self.name}'s turn. Enter column to drop ball: " )

		if not column.isdigit():
			raise ValueError

		column = int(column)
		self.game.move(column)


class AIController(Controller):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.SCORE = 10
		self.DEPTH = kwargs.get('max_depth', 5)


	def move(self):
		super().move()

		print(f"{self} thinking...")
		move = self._make_best_move()

		self.game.move(move)


	def _make_best_move(self):	
		if self.game.current_player["controller"] == self:
			ai_mark 			= self.game.current_player["mark"]
			opponent_mark = self.game.previous_player["mark"]

		else:
			ai_mark = self.game.previous_player["mark"]
			opponent_mark = self.game.current_player["mark"]

		board = copy.deepcopy(self.game.board)

		best_val = -math.inf
		best_move = None

		if board.plays < 1:
			return board.get_possible_moves(shuffle=True)[0]


		for move in board.get_possible_moves(shuffle=True):
			child = copy.deepcopy(board)
			child.play(ai_mark, move)

			move_val = self._minimax(child, False, 0, -math.inf, math.inf, ai_mark=ai_mark, opponent_mark=opponent_mark)

			# print(move, best_val, move_val)
			if move_val > best_val:
				best_val = move_val
				best_move = move

		return best_move


	def _evaluate(self, node, **kwargs):
		# node.print()
		# time.sleep(0.5)
		last_played = node.last_played
		if node.check(last_played):
			mark = node.get_at_played(last_played)
			if mark == kwargs['ai_mark']:
				return self.SCORE

			return -self.SCORE
		return 0


	def _minimax(self, node, is_max, depth, alpha, beta, **kwargs):
		score = self._evaluate(node, **kwargs)

		if abs(score) == self.SCORE:
			return score

		if node.plays >= node.MAX_COL * node.MAX_ROW:
			return 0

		if depth > self.DEPTH:
			return 0

		if is_max:
			max_eval = -math.inf
			for move in node.get_possible_moves(shuffle=True):
				if not node.is_column_full(move - 1):
					child = copy.deepcopy(node)
					child.play(kwargs['ai_mark'], move)

					eval = self._minimax(child, not is_max, depth + 1, alpha, beta, **kwargs)
					max_eval = max(max_eval, eval)

					alpha = max(alpha, max_eval)
					if alpha >= beta:
						break


			return max_eval

		else:
			min_eval = math.inf
			for move in node.get_possible_moves(shuffle=True):
				if not node.is_column_full(move - 1):
					child = copy.deepcopy(node)
					child.play(kwargs['opponent_mark'], move)

					eval = self._minimax(child, not is_max, depth + 1, alpha, beta, **kwargs)
					min_eval = min(min_eval, eval)
					
					beta = min(beta, min_eval)
					if beta <= alpha:
						break

			return min_eval




