import os
from .board import Board


class Game:
	def __init__(self, clr_console=False):
		self._players = {}
		self.turn = 0
		self.clr_console = clr_console
		self.won = False
		self.messages = []

	def setup(self):
		self.board = Board(rows=6, columns=7)
		self.won = False


	def add_players(self, *args, **kwargs):
		marks 			= [ "\U0001F630", "\U0001F621"]
		ai_marks = [u"\U0001F916", u"\U0001F47D"]
		human_count = 0
		ai_count 		= 0

		for idx, controller in enumerate(args):
			player_count = human_count + ai_count 
			mark = marks[player_count]

			match controller.__name__:
				case "HumanController":
					human_count += 1

					name = f"Player {human_count}"

				case "AIController":
					mark = ai_marks[ai_count]
					ai_count += 1
					name = f"Bot {ai_count if ai_count > 0 else None}"

				case _:
					break


			if player_count < 2:
				self._players[str(idx)] = {
					"score": 0,
					"controller": controller(game=self, name=name, **kwargs),
					"mark": mark
				}


	def next(self, commit=True):
		turn = 1 if self.turn == 0 else 0		
		if commit:
			self.turn = turn

		return turn 


	@property
	def players(self):
		return [ v for v in self._players.values() ]

	
	@property
	def current_player(self):
		return self._players[str(self.turn)]


	@property
	def previous_player(self):
		return self._players[str(self.next(commit=False))]


	def print(self):
		if self.clr_console:
			os.system('cls') if os.name == 'nt' else os.system('clear')

		print("*" * 50)

		for player in self.players:
			print(f"{player['controller']} -> {player['mark']} | score: {player['score']}")

		print("Moves played:", self.board.plays)
		print("*" * 50)
		self.board.print()

		for message in self.messages:
			print(message["message"])

		self.messages.clear()


	def move(self, move: int):
		if self.won == True:
			return 

		if self.board.plays >= 42:
			return False

		try:
			self.board.play(self.current_player["mark"], move)

			if self.board.check(move):
				self.won = True
				return
			
			self.next()
			self.current_player['controller'].move()

		except ValueError as e:
			self.messages.append({'type': 'error', 'message': e })
			self.current_player['controller'].move()


	def loop(self):
		self.setup()
		self.current_player['controller'].move()

		self.print()

		if self.won:
			print(f"{self.current_player['controller']} wins")
			self.current_player['score'] += 1

		else:		
			print("Game is a draw.")

		self.next()

