import pdb; import pickle; import os; import time; from enemy_images import monster_images

class Game():
	"""Game class; main element of the game"""
	def __init__(self, player):
		self.player = player
		self.primitive_options = {'i': [inventory.print_menu, self.player.inventory], 'room message': [self.player.print_room_menu, None]} # Functions that have no input, simply display information 

	def game_loop(self):
		self.player.print_room_menu()
		self.check_for_enemy()
		self.handle_user_input()

	def handle_user_input(self):
		while True:
			print("What will you do?")
			user_input_list = input('>>> ').lower().split()
			user_input = ''
			verb = ''
			noun = ''

			if len(user_input_list) == 1:
				user_input = user_input_list[0]
				if user_input in self.primitive_options.keys():
					if self.primitive_options[user_input][1]:
						self.primitive_options[user_input][0](self.primitive_options[user_input][1])
					else:
						self.primitive_options[user_input][0]()
				elif user_input == '':
					pass
				else:
					print("Invalid option!")
					
			elif len(user_input_list) > 1:
				verb = user_input_list[0]
				noun = " ".join(user_input_list[1:])
				
			if verb == 'take':
				self.player.take_item(self.player.current_room.remove_item(noun))
					
			elif verb == 'go' or verb == 'go to':
				self.player.move_rooms(noun)
					
			elif verb == 'back' or verb == 'go back':
				self.player.go_back()
					
			elif verb == 'equip':
				self.player.change_equipment(self.player.get_object(noun))

			elif verb == '':
				pass
					
			else:
				print("Invalid Input!")
		
	def check_for_enemy(self):
		for npc in self.player.current_room.npcs:
			if type(npc) == Enemy:
				combat.active_combat()




class Combat():
	"""Turn based rpg style combat
	Note: Place this inside game class or leave it here?"""
	def active_combat(self, opponent, player, player_turn = True ):
		print("A " + opponent.name + " appears")
		while player.health > 0 and opponent.health > 0:
			time.sleep(1.5)
			os.system('clear')
			print(opponent.image)
			print("_" * 28)
			print("Enemy health : " + "[+]" * int(opponent.health / 5))
			print("Your  health : " + "[+]" * int(player.health / 5))
			print("_" * 28)
			self.print_combat_panel(player)
			while player_turn:
				print("What will you do?")
				user_input = input('>>> ')
				user_input_list = user_input.split()
				if user_input in player.weapon.attacks.keys():
					player.attack(opponent, user_input)
					player_turn = False
				elif user_input == 'i':
					inventory.print_menu(player.inventory)
				elif user_input_list[0] == 'use' and " ".join(user_input_list[1:]) in [item.name for item in player.inventory]:
					player.inventory[user_input_list[1]].special_property_use(player)
				else:
					print("Invalid option (in active_combat)")                
			opponent.attack(player)
			player_turn = True

	def print_combat_panel(self, player):
		print("_" * 28)
		print("-----------COMBAT-----------")
		print("_" * 28)
		print("ATTACK----------------DAMAGE")
		for key, val in player.weapon.attacks.items():
			print(key + " " * (26 - len(key + str(val))) + str(val) + " |")
		print("_" * 28)



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
		if item in self.items.keys():
			return self.items.pop(item)
		else:
			return None



class Player():
	"""docstring for Player"""
	def __init__(self, name, health, gold, inventory, current_room):
		self.name = name
		self.health = health
		self.gold = gold
		self.inventory = inventory
		self.current_room = current_room
		self.previous_rooms = []
		self.equipment = {'head': None, 'chest': None, 'legs': None, 'weapon': None}
		
		
	def print_room_menu(self): 
		print("_" * 28)
		self.current_room.print_room_message()
		self.current_room.print_exits()
		self.current_room.print_items()
		self.current_room.print_npcs() 
		print("_" * 28)

	def take_item(self, item):
		if item:
			self.inventory.append(item)
			print("You took %s" %(item.name))
		else:
			print("That item is not in this room")
			
	def move_rooms(self, next_room_dir):
		if next_room_dir in self.current_room.exits.keys():
			self.previous_rooms.append(self.current_room)
			self.current_room = self.current_room.exits[next_room_dir]
			self.print_room_menu()
		else:
			print("Not a valid room!")
			
	def go_back(self):
		if len(self.previous_rooms) > 0:
			self.current_room = self.previous_rooms.pop()
			self.print_room_menu()
		else:
			print("You cannot go back!")
			
	def change_equipment(self, item_to_equip):
		if item_to_equip:
			if type(item_to_equip) == Weapon:
				self.equipment['weapon'] = item_to_equip
				print("You equipped %s" % item_to_equip.name)
			elif type(item_to_equip) == Armor:
				self.equipment[item_to_equip.armor_type] = item_to_equip
				print("You equipped %s" % item_to_equip.name)
			else:
				print("That item is not equipabble.")
		else:
			print("You do not have that item to equip, or you spelled it wrong. Please try again.")

	def attack(self, attack):
		if self.equipment['weapon']:
			return self.equipment['weapon'].attacks[attack]
		else:
			print("You have no weapon! You cannot attack")
			return 0
			
	def get_object(self, checking_item):
		items_dict = {item.name.lower(): item for item in self.inventory}
		if checking_item.lower() in items_dict.keys():
			return items_dict[checking_item]
		else:
			return None



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
		print("_" * 28)
		print(self.name)
		print("_" * 28)
		for item in menu_components:
			print(item.name)
		print("_" * 28)


inventory = Menu("INVENTORY")

# SpecialItem instaces
amulet = SpecialItem(
	'amulet',
	'This is an amulet',
	0,
	None,
	0,
	10
	)

# Weapon Instances
longsword = Weapon(
	'Longsword',
	'Longsword description',
	{'side swipe': 15},
	5
	)
	
# Armor instances
iron_helm = Armor(
	'Iron Helmet',
	'This is some armor',
	5,
	'head',
	10
	)

# Room instances
test_room2 = Room(
	"Test Room 2",
	"Another Test room",
	{},
	[],
	[]
	)
	
test_room = Room(
	"Test Room",
	"this is a test",
	{"north": test_room2},
	[amulet],
	[]
	)
	
combat = Combat()
player = Player('Sean', 100, 20, [iron_helm], test_room)
game = Game(player)
game.game_loop()
