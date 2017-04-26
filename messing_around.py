import pdb

class Game():
	"""Game class; main element of the game"""
	def __init__(self, player):
		self.player = player

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
			user_input = ''
			if len(user_input_list) == 1:
				user_input = user_input_list[0]
			elif len(user_input_list) > 1:
				pdb.set_trace()
				verb = user_input_list[0]
				noun = " ".join(user_input_list[1:])

			if user_input == 'i':
				inventory.print_menu(self.player.inventory)

			elif user_input == 'health':
				print(self.player.health)

			elif verb == 'take' and noun in self.player.current_room.items.keys():
				self.player.take_item(self.player.current_room.remove_item(noun))

			else:
				print("Invalid Input!")




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
		self.items = {item.name: item for item in items}
		self.npcs = {npc.name: npc for npc in npcs}

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
	def __init__(self, name, health, gold, inventory, current_room):
		self.name = name
		self.health = health
		self.gold = gold
		self.inventory = inventory
		self.current_room = current_room

	def take_item(self, item):
		pdb.set_trace()
		self.inventory.append(item)
		print("You took %s" %(item.name))



class NPC():
    def __init__(self, name, health, greeting, weapon, pacifist):
        self.name = name
        self.health = health
        self.greeting = greeting
        self.weapon = weapon
        self.pacifist = pacifist



class Merchant(NPC):
    def __init__(self, name, health, greeting, weapon, pacifist, inventory, guards):
        self.name = name
        self.health = health
        self.greeting = greeting
        self.weapon = weapon
        self.pacifist = pacifist
        self.inventory = inventory
        self.guards = guards



class Enemy():
    def __init__(self, name, health, greeting, image, weapon, armor):
        self.name = name
        self.health = health
        self.greeting = greeting
        self.image = image
        self.weapon = weapon
        self.armor = armor	


class SpecialItem():
    def __init__(self, name, description, damage, special_property, special_val, cost):
        self.name = name
        self.description = description
        self.damage = damage
        self.special_property = special_property
        self.special_val = special_val
        self.cost = cost



class Weapon():
    def __init__(self, name, description, attacks, cost):
        self.name = name
        self.description = description
        self.attacks = attacks
        self.cost = cost



class Armor():
    def __init__(self, name, description, defense, armor_type, cost):
        self.name = name
        self.description = description
        self.defense = defense
        self.armor_type = armor_type
        self.cost = cost


class Menu():
	"""docstring for Menu"""
	def __init__(self, name):
		self.name = name

	def print_menu(self, menu_components):
		print(self.name)
		for item in menu_components:
			print(item)


inventory = Menu("INVENTORY")

# SpecialItem instaces
amulet = SpecialItem(
	'Amulet',
 	' This is an amulet',
 	0,
 	None,
 	0,
 	10)

# Room instances
test_room = Room(
	"Test Room",
	"this is a test",
	{},
	[amulet],
	{}
	)

player = Player('Sean', 100, 20, [], test_room)
game = Game(player)
game.game_loop()
