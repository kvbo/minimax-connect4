from lib.game import Game
from lib.controllers import HumanController, AIController


def main():
	game = Game(clr_console=True)	
	game.add_players(AIController, AIController, max_depth=3)
	# game.add_players(HumanController, HumanController)


	while True:
		game.loop()
		response = str(input("Press (Y) to continue. "))
		
		if response.lower() != 'y':
			break


if __name__ == "__main__":
	main()