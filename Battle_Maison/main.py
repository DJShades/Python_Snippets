import os
from random import choice as rc
from time import sleep 

rooms_map = [
	{'name':'Entrance hall',
	 'floor':0,
	 'idx':0,
	 'connecting':[1,3,4,6]
	},
	{'name':'Lounge',
	 'floor':0,
	 'idx':1,
	 'connecting':[0,2]
	},
	{'name':'Dining room',
	 'floor':0,
	 'idx':2,
	 'connecting':[1,3]
	},
	{'name':'Kitchen',
	 'floor':0,
	 'idx':3,
	 'connecting':[0,2]
	},
	{'name':'Laundry room',
	 'floor':0,
	 'idx':4,
	 'connecting':[0,5]
	},
	{'name':'Garage',
	 'floor':0,
	 'idx':5,
	 'connecting':[4,15]
	},
	{'name':'Stairs',
	 'floor':0.5,
	 'idx':6,
	 'connecting':[0,7]
	},
	{'name':'Landing',
	 'floor':1,
	 'idx':7,
	 'connecting':[6,8,10,12,13,14]
	},
	{'name':'Master bedroom',
	 'floor':1,
	 'idx':8,
	 'connecting':[7,9]
	},
	{'name':'Master bedroom ensuite',
	 'floor':1,
	 'idx':9,
	 'connecting':[8]
	},
	{'name':'2nd bedroom',
	 'floor':1,
	 'idx':10,
	 'connecting':[7,11]
	},
	{'name':'2nd bedroom ensuite',
	 'floor':1,
	 'idx':11,
	 'connecting':[10]
	},
	{'name':'Guest bedroom',
	 'floor':1,
	 'idx':12,
	 'connecting':[7]
	},
	{'name':'Bathroom',
	 'floor':1,
	 'idx':13,
	 'connecting':[7]
	},
	{'name':'Office',
	 'floor':1,
	 'idx':14,
	 'connecting':[7]
	},
	{'name':'Garden',
	 'floor':0,
	 'idx':15,
	 'connecting':[5,3,16]
	},
	{'name':'Garden shed',
	 'floor':0,
	 'idx':16,
	 'connecting':[15]
	}			    
]

class Game:
	
	def __init__(self,game_map):
		self.players = []
		self.active_player = None
		self.rooms = self._setup_rooms(game_map)
		self.running = False

	def add_player(self, player):
		self.players.append(player)
		player.set_idx(self.players.index(player))

	def remove_player(self, player):
		self.players.pop(self.players.index(player))
		for player in self.players:
			player.set_idx(self.players.index(player))
		return True

	def start(self):
		if len(self.players) > 1:
			self._randomise_starting_player()
			self.running = True
			return self.running

	def _randomise_starting_player(self):
		self.active_player = rc(self.players)

	def next_player(self):
		active_player_idx = self.players.index(self.active_player)
		if active_player_idx < len(self.players)-1:
			self.active_player = self.players[active_player_idx+1]
		else:
			self.active_player = self.players[0]

	def _setup_rooms(self, game_map):
		rooms = []
		for room in game_map:
			rooms.append(Room(room['name'], room['floor'], room['idx'], room['connecting']))
		return rooms

	def reset(self):
		for player in self.players:
			player.init()
		for room in self.rooms:
			room.init()


class Player:
	
	def __init__(self, name):
		self.name = name
		self.idx = -1
		self.init()

    # Things that can be reset without re-instantiating the player object.
	def init(self):
		self.location = self._spawn()
		self.weapons = []

	def _spawn(self):
		# Prevents any two players from spawning in same location
		rooms = game.rooms.copy()
		for player in game.players:
			rooms.pop(rooms.index(player.location))
		return rc(rooms)

	def set_idx(self, idx):
		self.idx = idx

	def move(self, location):
		self.location = location


class Room:
	
	def __init__(self, name, floor, idx, connecting):
		self.name = name
		self.floor = floor
		self.idx = idx
		self.connecting = connecting
		self.init()

    # Things that can be reset without completely re-instantiating the room object(s)
	def init(self):
		self.weapons = []
		self.traps = []


# Class used as namespace only!
class location:

	@staticmethod
	def show(player):
		preposition = 'on' if player.location.name in ('Landing', 'Stairs') else 'in' 
		print(f'{player.name} is {preposition} the {player.location.name.lower()}')

	@staticmethod
	def show_connections(player):
		print(f'Choose a destination:')
		for idx, room_idx in enumerate(player.location.connecting):
			print(f'  {idx+1}: {game.rooms[room_idx].name}')

	@staticmethod
	def move(player):
		location.show_connections(player)
		options = [game.rooms[idx] for idx in player.location.connecting]
		room = utils.selector(options, location.move_error)
		player.move(room)
		print(f'{player.name} moved to the {player.location.name.lower()}')
		sleep(3)
		os.system('cls')

	def move_error(_ignore):
		sleep(3)
		os.system('cls')
		location.show(game.active_player)
		location.show_connections(game.active_player)


# Class used as namespace only!
class utils:

	@staticmethod
	def selector(options, error_handler, selection=-1):
		# This doesn't "feel" right, but it works...
		while selection < 0 or selection > len(options)-1:
			try:
				selection = int(input('Selection: '))-1
			except ValueError:
				print('Input must be a number, please try again')
				error_handler(options)
			else:
				if selection < 0 or selection > len(options)-1:
					print('Not a valid selection, please try again')	
					error_handler(options)
		else:
			return options[selection]


# Class used as namespace only!
class menu:

	@staticmethod
	def main():
		os.system('cls')
		options = [('Player setup', menu.player_setup), ('Start Game', menu.game_start)]
		menu.show_options([option[0] for option in options])
		func = utils.selector(options, menu.main_error)[1]
		# This "feels" wrong... but it works.
		func()

	def main_error(options):
		sleep(3)
		os.system('cls')
		menu.show_options([option[0] for option in options])
	
	@staticmethod
	def player_setup():
		os.system('cls')
		menu.show_players()
		
		options = [('Add player', menu.add_player)]
		if len(game.players) > 0: options.append(('Remove player', menu.remove_player))
		options.append(('Back to main menu', menu.main))
		
		menu.show_options(option[0] for option in options)
		func = utils.selector(options, menu.player_setup_error)[1]
		func()

	def player_setup_error(options):
		sleep(3)
		os.system('cls')
		menu.show_players()
		menu.show_options(option[0] for option in options)

	@staticmethod
	def add_player():
		os.system('cls')
		player_name = input('Enter player name: ')
		game.add_player(Player(player_name))
		menu.player_setup()

	@staticmethod
	def remove_player():
		os.system('cls')
		menu.show_options([player.name for player in game.players], msg='Select a player to remove:')
		player = utils.selector(game.players, menu.remove_player_error)
		game.remove_player(player)
		menu.player_setup()

	def remove_player_error(options):
		sleep(3)
		os.system('cls')
		menu.show_options([player.name for player in game.players], msg='Select a player to remove:')

	@staticmethod
	def game_start():
		if game.start():
			while game.running:
				os.system('cls')
				location.show(game.active_player)
				location.move(game.active_player)
				game.next_player()
		else:
			print('You need at least two players to start the game!')
			sleep(3)
			os.system('cls')
			menu.main()

	def show_options(options, msg='Choose an option:'):
		print(msg)
		for idx, option in enumerate(options):
		    print(f'  {idx+1}: {option}')

	def show_players():
		print('Players:')
		if game.players:
			for player in game.players:
				print(f'  {player.name}')
		else:
			print('  None')


if __name__ == '__main__':

	# If loading different room maps is implemented, it will be handled via a
	# Game class method. For now the one map available is loaded at Game class 
	# instanciation. And yes, I know, the current map is held in a Global.
	game = Game(rooms_map)
	menu.main()
    
