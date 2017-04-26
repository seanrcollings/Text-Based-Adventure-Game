import pdb

class Game():
	"""Game class main element of the game"""
	def __init__(self, player):
		self.player = player
		self.possible_options = {'take': self.player.current_room.remove_item}

	def game_loop(self):
		self.print_room_menu()
		self.handle_user_input()

	def print_room_menu(self): 
		print("_" * 28)
		self.player.current_room.print_room_message()
		self.player.current_room.print_exits()
		self.player.current_room.print_items()
		self.player.current_room.print_npcs() 
		print("_" * 28)

	def handle_user_input(self):
		while True:
			print("What will you do?")
			user_input_list = input('>>> ').lower().split()
			verb = user_input_list[0]
			noun = " ".join(user_input_list[1:])

			if verb in self.possible_options.keys():	
				self.possible_options[verb](noun)



class Combat():
	"""docstring for Combat"""
	def __init__(self, arg):
		self.arg = arg		



class Room():
	"""Room class: location of the player, and all the things they can interact with in that enviorment"""
	def __init__(self, name, room_message, exits, items, npcs):
		self.name = name
		self.room_message = room_message
		self.exits = exits
		self.items = items
		self.npcs = npcs

	def print_room_message(self):
		print(self.room_message)

	def print_exits(self):
		if len(self.exits) == 0:
			print("There are no apparent exits, besides the one you entered.")
		else:
			print("The exits in the room are: %s " % ", ".join(self.exits.keys()))

	def print_items(self):
		if len(self.items) == 0:
			print("The room appears to be bare of anything useful to you.")
		else:
			print("The items in the room are: %s " % (", ".join(self.items.keys())))

	def print_npcs(self):
		if len(self.npcs) == 0:
			print("The room is empty of human presence")
		else:
			print("The people in the room are: %s " % (", ".join(self.npcs.keys())))

	def remove_item(self, item):
		pdb.set_trace()
		if item in self.items.keys():
			return self.items.pop(item)
		else:
			print("That item is not in this room")



class Player():
	"""docstring for Player"""
	def __init__(self, current_room, inventory):
		self.current_room = current_room
		self.inventory = inventory


class NPC():
	"""docstring for NPC"""
	def __init__(self, arg):
		self.arg = arg



class Merchant(NPC):
	def __init__(self, arg):
		self.arg = arg



class Enemy(NPC):
	"""docstring for Enemy"""
	def __init__(self, arg):
		self.arg = arg		


class SpecialItem():
	"""docstring for Itema"""
	def __init__(self, arg):
		self.arg = arg



class Weapon():
	"""docstring for Weapon"""
	def __init__(self, arg):
		self.arg = arg



class Armor():
	"""docstring for Armor"""
	def __init__(self, arg):
		self.arg = arg


class Menu():
	"""docstring for Menu"""
	def __init__(self, arg):
		self.arg = arg



test_room = Room(
	"Test Room",
	"this is a test",
	{},
	{"test_name": "test_key"},
	{}
	)

player = Player(test_room, [])
game = Game(player)
game.game_loop()
