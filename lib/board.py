import time
import random


class Board:
	def __init__(self, **kwargs):
		self.MAX_COL = kwargs.get('columns', 7)
		self.MAX_ROW = kwargs.get('rows', 6)

		self.none_str = "  "
		self.plays = 0
		# 
		self.board = [
			[self.none_str] * self.MAX_ROW,
		] * self.MAX_COL

		self._last_played = []


	@property
	def last_played(self):
		return self._last_played[-1]

	
	@last_played.setter
	def last_played(self, val):
		self._last_played.append(val)


	def play(self, mark: str, column: int):
		if column < 1 or column > self.MAX_COL :
			raise ValueError


		_column = column - 1


		# print(self.print())
		if not self.is_column_full(_column):
			self.insert(_column, mark)

			self.plays += 1
			self.last_played = _column

		else:
			raise ValueError


	def undo(self):
		popped = self._last_played.pop()
		for idx, val in enumerate(self.board[popped]):
			if val != self.none_str:
				self.board[popped][idx] = self.none_str

		self.plays -= 1


	def undo_at(self, last_played):
		column = last_played - 1
		for idx, val in enumerate(self.board[column]):
			if val != self.none_str:
				self.board[column][idx] = self.none_str	

		self.plays -= 1


	def insert(self, column, mark	):
		empty_row = None
		last_index = self.MAX_ROW - 1

		for idx, row in enumerate(self.board[column]):
			if row != self.none_str:
				empty_row = idx - 1
				break

			if idx == last_index:
				empty_row = idx 
				break

		if empty_row >= 0:
			temp = self.board[column].copy()
			temp[empty_row] = mark

			self.board[column] = temp


	def is_column_full(self, column: int) -> bool:
		if self.none_str in self.board[column]:
			return False

		return True


	def print(self):
		print("")
		print("   " + "    ".join([str(i) for i in range(1, self.MAX_COL + 1)] ))	
		print("", "---- " * self.MAX_COL)

		for row in range(self.MAX_ROW):
			col = []
			for column in range(self.MAX_COL):
				col.append(self.board[column][row])
			

			print("|", " | ".join(col), "|")
			print("", "---- " * self.MAX_COL)

		print("")


	def copy(self):
		return self.board.copy()


	def check(self, last_played) -> bool:
		row = None
		column = self.last_played

		for idx, val in enumerate(self.board[column]):
			if val != self.none_str:
				row = idx
				break

		if self._check_column_row(row, column):
			return True


		if self._check_diagonals(row, column):
			return True
		return False


	def get_at(self, row, column):
		val = self.board[column][row]
		if val != self.none_str:
			return val	

		return None


	def get_at_played(self, last_played):
		match = filter(lambda x: x != self.none_str, self.board[last_played])
		return next(match, self.none_str)


	def _check_column_row(self, row, column):
		mark = self.get_at(row, column)		

		if mark is None:
			return False

		vis = [ False, False, False, False ]

		start_c = column
		end_c = column

		start_r = row
		end_r = row

		count = 1

		while False in vis:
			if not vis[1]:
				depth = row + count
				if depth < self.MAX_ROW and self.board[column][depth] == mark:
					end_r = depth

				else:
					vis[1] = True


			if not vis[0]:
				depth = row - count

				if depth >= 0 and self.board[column][depth] == mark:
					start_r = depth

				else:
					vis[0] = True


			if not vis[2]:
				depth = column + count
				if depth < self.MAX_COL and self.board[depth][row] == mark:
					end_c = depth

				else:
					vis[2] = True


			if not vis[3]:
				depth = column - count

				if depth >= 0 and self.board[depth][row] == mark:
					start_c = depth

				else:
					vis[3] = True

			count += 1


		if abs(start_r - end_r) >= 3:
			return True

		if abs(start_c - end_c) >= 3:
			return True
				
		return False


	def _check_diagonals(self, row, column):
		mark = self.get_at(row, column)		

		if mark is None:
			return False

		vis = [ False ] * 4

		major_start_c = column
		major_start_r = row
		major_end_c = column
		major_end_r = row

		minor_start_r = row
		minor_start_c = column
		minor_end_r = row
		minor_end_c = column		


		count = 1
		while False in vis:

			# Major
			if not vis[1]:
				depth_r = row + count
				depth_c = column + count

				if depth_r < self.MAX_ROW and depth_c < self.MAX_COL and self.board[depth_c][depth_r] == mark:
					major_end_r = depth_r
					major_end_c =depth_c

				else:
					vis[1] = True


			if not vis[0]:
				depth_r = row - count
				depth_c = column - count

				if depth_r >= 0 and depth_c >= 0 and self.board[depth_c][depth_r] == mark:
					major_start_r = depth_r
					major_start_c = depth_c

				else:
					vis[0] = True

			# Minor
			if not vis[3]:
				depth_r = row - count
				depth_c = column + count

				if depth_r >= 0 and depth_c < self.MAX_COL and self.board[depth_c][depth_r] == mark:
					minor_start_r = depth_r
					minor_end_c = depth_c

				else:
					vis[3] = True


			if not vis[2]:
				depth_r = row + count
				depth_c = column - count

				if depth_r < self.MAX_ROW and depth_c >= 0 and self.board[depth_c][depth_r] == mark:
					minor_end_r = depth_r
					minor_start_c = depth_c

				else:
					vis[2] = True

			count += 1


		if abs(minor_start_c - minor_end_c) == abs(minor_start_r - minor_end_r) >= 3:
			return True

		if abs(major_start_c - major_end_c) == abs(major_start_r - major_end_r) >= 3:
			return True

		return False


	def get_possible_moves(self, shuffle=False):
		possible_moves = []
		if self.plays < self.MAX_COL * self.MAX_ROW:
			for idx, column in enumerate(self.board):
				if self.none_str in column:
					possible_moves.append(idx + 1)

		if shuffle:
			random.shuffle(possible_moves)

		return possible_moves
		
	