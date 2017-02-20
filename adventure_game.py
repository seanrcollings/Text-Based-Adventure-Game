import sys
import pdb
import time
import pickle


################
# ITEM CLASSES #
################

class Weapon():
    def __init__(self, name, description, damage, cost):
        self.name = name
        self.description = description
        self.damage = damage
        self.cost = cost


    """def use_wpn_art(self, npc_to_attack):
        self.damage *= 2"""  


class SpecialItem():
    def __init__(self, name, description, damage, special_property, cost):
        self.name = name
        self.description = description
        self.damage = damage
        self.special_property = special_property
        self.cost = cost

    def special_property_use(self, current_room):
        if self.special_property == "reveal":
            current_room.print_secret()
        elif self.special_property == "no effect":
            print("You blimey fool! Waving that around like it's a magic wand! No effect!")
        else:
            print("This item is not usable in this way")



class Armor():
    def __init__(self, name, description, defense, armor_type, cost):
        self.name = name
        self.description = description
        self.defense = defense
        self.armor_type = armor_type
        self.cost = cost
        

    def calc_damage_reduction(self, weapon):
        reduction_percent = weapon.damage * self.defense
        new_damage = weapon.damage - reduction_percent
        return new_damage



######################
# CLASSES FOR PEOPLE #
######################

class NPC():
    def __init__(self, name, health, greeting, weapon, friendly, pacifist):
        self.name = name
        self.health = health
        self.greeting = greeting
        self.weapon = weapon
        self.friendly = friendly
        self.pacifist = pacifist

    def print_greeting(self):
        print(self.greeting)

    def attack(self, npc_to_attack):
        if not self.pacifist:
            npc_to_attack.health -= self.weapon.damage

    def interact_with_player(self):
        pass
        


class Merchant(NPC):
    def __init__(self, name, health, greeting, weapon, friendly, pacifist, inventory, guards):
        self.name = name
        self.health = health
        self.greeting = greeting
        self.weapon = weapon
        self.friendly = friendly
        self.pacifist = pacifist
        self.inventory = inventory
        self.guards = guards

    # TODO: if input is invalid, allow them to try again
    def buy(self, player):
        buying_input = input().split()
        verb = buying_input[0]
        noun = " ".join(buying_input[1:])
        if len(buying_input) != 2:
            print("In order to buy, say 'buy (item)'")
            print("In order to sell, say 'sell (item)'")
        elif verb == "buy" and noun in self.inventory.keys():
            # TODO: error message if the merchant does not have the item
            item = self.inventory[noun]
            player.inventory.append(item)
            player.gold -= item.cost
            del self.inventory[noun]
            print("You bought " + noun)
        elif verb == "sell" and noun in player.items_dictionary().keys():
            player.inventory.remove(player.items_dictionary[noun])
            player.gold += player.items_dictionary[noun].cost
            print("You sold " + noun) 

    def attack(self, attacking_npc):
        if not self.pacifist:
            guards.attack(attacking_npc)

    def interact_with_player(self, player):
        self.print_greeting()
        merchant_inventory.print_menu(self.inventory)
        self.buy(player)
  

class Game():
    def __init__(self, starting_room, all_rooms, all_items, all_npcs, player):
        self.all_rooms = all_rooms
        self.all_items = all_items
        self.all_npcs = all_npcs
        self.current_room = starting_room
        self.previous_rooms = []
        self.player = player

    def game_loop(self):
        self.print_room_messages()
        self.handle_user_input()

    def slow_text(self, text): # Don't like how this works, need a way for it just to print everything at once if a button is pressed (Threading?)
        for letter in text:
            sys.stdout.write(letter)
            sys.stdout.flush()
            time.sleep(.03)
        print('\n')

    def print_room_messages(self):
        print(UNDERLINES)
        self.current_room.print_welcome()
        self.current_room.print_exits()
        self.current_room.print_items()
        self.current_room.print_npcs()
        print(UNDERLINES)

    def help_function(self):
        print("TIPS")
        print("Type 'i' to open your inventory")
        print("Type 'save' to save your progress ")
        print("Type 'g' to check your gold stash")
        print("Type 'health' to check your health")
        print("Type 'exit' to quite the game")
    
    def handle_user_input(self):
        possible_adjectives = ["with"] # Temporary fix for entering handle_language twice with the 2 if statements below, working and the printing the fail state. 
        while player.health > 0:
            print("\n")
            user_input_list = input(">>> ").split()
            user_input = ''
            if len(user_input_list) == 1:
                user_input = user_input_list[0]
            
            elif len(user_input_list) >= 2 and user_input_list[1] not in possible_adjectives:
                self.handle_language(" ".join(user_input_list[1:]), user_input_list[0].lower())
        
            elif len(user_input_list) >= 3 and user_input_list[1] in possible_adjectives: # Temporary fix for interacting with NPCs, change to account for this in the previous statment later
                self.handle_language(" ".join(user_input_list[2:]), user_input_list[0].lower(), user_input_list[1])

            if user_input == 'i': 
                inventory.print_menu(self.player.inventory)                                                

            elif user_input == 'g':
                print(str(self.player.gold))

            elif user_input == 'back':
                self.current_room = self.previous_rooms.pop()
                self.print_room_messages()

            elif user_input == 'save':
                save_info = {
                "player": self.player,
                "current room": self.current_room,
                "previous rooms": self.previous_rooms,
                }
                save_file = open("save.pkl", "wb")
                pickle.dump(save_info, save_file)
                print("You saved in: " + self.current_room.name)   
                save_file.close()

            elif user_input == 'health':
                print("Your health is: " + str(self.player.health))

            elif user_input == 'exit':
                print("Goodbye!")
                sys.exit(0)        

            elif user_input == 'help':
                self.help_function()

            elif user_input == '':
                pass

            else:
                print("Invalid option!(In handle_user_input)")

        print("YOU DIED")


    def handle_language(self, noun, verb, adjective = ""):
        """Handles more than 1 word inputs, usually in the form of verb adjective(optional) noun"""
        
        room_npcs  = [npc.name for npc in self.current_room.npcs]

        if verb == 'take' and noun in self.current_room.items.keys():
            self.player.inventory.append(self.all_items_dictionary()[noun])
            print("You took " + noun)
        
        elif verb == 'interact' and adjective == 'with' and noun in room_npcs:
            self.all_npcs_dictionary()[noun].interact_with_player(player)
        
        elif verb == 'go' and noun in self.current_room.exits.keys():
            self.previous_rooms.append(self.current_room)
            self.current_room = self.current_room.exits[noun]
            self.print_room_messages()

        elif verb == 'equip' and noun in self.player.items_dictionary().keys():
             self.player.change_equipment(noun)

        elif verb == 'attack' and noun in self.current_room.npcs.keys():
            npc_to_attack = self.current_room.npcs[noun]
            self.player.attack(npc_to_attack)
    
        elif verb == 'use' and noun in self.player.items_dictionary().keys():
            self.all_items_dictionary()[noun].special_property_use(self.current_room)

        elif verb == 'check' and noun in self.player.items_dictionary().keys():
            print(player_items[noun].description)

        elif verb == 'check' and noun == 'equipment':
            print("Weapon:   " + self.player.weapon.name)
            print("Head:     " + self.player.armor["head"].name)
            print("Chest:    " + self.player.armor["chest"].name)
            print("Legs:     " + self.player.armor["legs"].name)

        elif verb == 'room' and noun == 'message':
            self.print_room_messages()

        else:
            print("Invalid option!(In handle_language)")

    def start(self):
        try:
            file = open('save.pkl', 'rb')
            load_file = pickle.load(file)
            load_input = input("It looks like you have a save in: \n" + load_file['current room'].name + "\nWould you like to load it?(y/n) \n")
            if load_input == 'y':
                print("Loading....")
                self.current_room = load_file['current room']
                self.previous_rooms = load_file['previous rooms']
                self.player = load_file['player']
                file.close()
                self.game_loop()
            else:
                file.close()
                self.intro()
        except EOFError:
            self.intro()

            
    def intro(self, save_inventory = ["Fists of Fury"]):
        self.save_inventory = save_inventory   
        print("TIPS")
        print("1. Press i will allow you to view your inventory")
        print("2. Typing save will allow you to save your game")
        print("3. You can acess the help at any time by typing help")
        confirm = input("Type y to start the game when you are ready!\n")      
        if confirm == "y":
            for word in self.save_inventory:
                item = self.all_items_dictionary()[word.strip('\n')]
                self.player.inventory.append(item)  
            self.game_loop()
        else:
            print("I don't belive you know how to work a computer!")

    def all_rooms_dictionary(self):
        all_rooms_dict = {}
        for room in self.all_rooms:
            all_rooms_dict[room.name] = room
        return all_rooms_dict

    def all_items_dictionary(self):
        all_items_dict = {}
        for item in self.all_items: 
            all_items_dict[item.name] = item
        return all_items_dict

    def all_npcs_dictionary(self):
        all_npcs_dict = {}
        for npc in self.all_npcs:
            all_npcs_dict[npc.name] = npc 
        return all_npcs_dict



class Player():
    def __init__(self, name, health, inventory, gold, weapon, armor):
        self.name = name
        self.health = health
        self.inventory = inventory
        self.gold = gold
        self.weapon = weapon
        self.armor = armor

    def npc_interactions(self):
        pass

    def attack(self, npc_to_attack):
        self.npc_to_attack = npc_to_attack
        if len(self.weapon.name) == 0:
            print("You have no weapon! You cannot attack")
        else:
            self.npc_to_attack.health -= self.weapon.damage
            if self.npc_to_attack.health <= 0:
                print("You killed " + self.npc_to_attack.name)
            else:
                print("You attacked " + npc_to_attack.name + " and did " + str(self.weapon.damage) + " damage.")
                npc_to_attack.attack(self)

    def change_equipment(self, item_to_equip):
        if type(self.items_dictionary()[item_to_equip]) is Weapon:
            self.weapon = self.items_dictionary()[item_to_equip]
            print("You equipped " + item_to_equip)
        elif type(self.items_dictionary()[item_to_equip]) is Armor:
            self.armor[self.items_dictionary()[item_to_equip].armor_type] = self.items_dictionary()[item_to_equip]
            print("You equipped " + item_to_equip)
        else:
            print("That item is not equipable.")
            
    def items_dictionary(self):
        player_items = {}
        for item in self.inventory:
            player_items[item.name] = item
        return player_items
        


class Room():
    def __init__(self, welcome_message, name, exits, items, npcs, secret):
        self.name = name
        self.welcome_message = welcome_message
        self.exits = exits
        self.items = items
        self.npcs = npcs
        self.secret = secret
        
    def print_welcome(self):
        print(self.welcome_message)
        
    def print_exits(self):
        if len(self.exits) ==  0:
            print("There are no apparent exits, besides the one you entered")
        else:
            print("The exit(s) are: " + ", ".join(self.exits.keys()))
        
    def print_items(self):
        if len(self.items) == 0:
             print("That are no items!")
        else:
            print("The item(s) are: " + ", ".join(self.items.keys()))

    def print_npcs(self):
        if len(self.npcs) == 0:
            print("There are no NPCs!")
        else:
            print("The people in the room are: " + ", ".join(npc.name for npc in self.npcs))

    def print_secret(self):
        if len(self.secret) == 0:
            print("No secrets to be found")
        else:
            print(self.secret)


class Area():
    def __init__(self, name, rooms):
        self.name = name
        self.rooms = rooms

    def print_area_name():
        if len(self.name) > 0:
            print(self.name)
        else:
            print("")



class Menu():
    def __init__(self, name):
        self.name = name

    def print_menu(self, menu_components):
        if type(menu_components) == list:
            print("_" * 28)
            print(self.name)
            print("_" * 28)    
            for item in menu_components:
                print(item.name + " " * (26 - len(item.name + str(item.cost))) + str(item.cost) + "g |")
            print("_" * 28)
        elif type(menu_components) == dict:
            print("_" * 28)
            print(self.name)
            print("_" * 28)         
            for key, val in menu_components:
                print(val.name + " " * (26 - len(val.name + str(val.cost))) + str(val.cost) + "g |")



###################
# CLASS INSTANCES #
###################

# Weapon Instances
# name, description, damage, cost
butterfly = Weapon(
    "Butterfly Sword",
    "A butterfly mounted to the hilt of the sword, whowever thought this was a bright idea must be quite mad. Why are you carrying it around? Maybe you're mad", 
    2,
    10
    )
longsword = Weapon(
    "Longsword", 
    "A longsword, simple, but dependable", 
    45, 
    12
    )
greatsword = Weapon(
    "Greatsword",
    "A massive blade that requires great strenght to lift. But can be used to crush your enemies into a pulp",
    89,
    20
    )
no_weapon = Weapon(
    "No Weapon", 
    "Does not possess a weapon. Does not belive in such tom foolery",
    0,
    0
    )

sword = Weapon("Sword",
    "A plain sword, made of steel in a human forge. A decent overall weapon.",
    40,
    10
    )
    
scythe = Weapon(
    "Scythe",
    "A farming tool, sharpened to extreme measures. Useful for trapping an enemy's weapon.",
    30,
    11
    )
    
fists_of_fury = Weapon(
    "Fists of Fury",
    "LISTEN UP, YOU PANSY. USE YOUR FISTS. PUNCH THEM INTO SUBMISSION!!!",
    9001,
    17
    )
    
gnomes = Weapon(
    "Infinite throwing gnomes",
    "You're a horrible person if you use this",
    100,
    10
    )
    
your_hammer = Weapon(
    "Your pitiful hammer",
    "You can't do anything with this, no wonder the ladies laugh at you.",
    -5,
    5
    )

# Special Item Instances
# name, description, damage, special property, cost    
eye_of_aganom = SpecialItem(
    "Eye of Aganom",
    "The Eye of Aganom is a powerful relic used to reveal secrets about a location.",
    0,
    "reveal",
    90
    )       

pendant = SpecialItem(
    "Pendant",
    "A simple pendant with no effect. Even so, pleasant memories are crucial to survival on arduous journeys.",
    0,
    "no effect",
    99999
    )  

# Armor instances
# name, description, defense, piece, cost
iron_helm = Armor(
    "Iron Helmet",
    "A simple, but dependable Iron Helmet",
    .25,
    "head",
    25
    )      

iron_chest = Armor(
    "Iron Chestplate",
    "A simple, but dependable Iron Chestplate",
    .30,
    "chest",
    25
    )

iron_legs = Armor(
    "Iron Leggings",
    "Simple, but dependable Iron Legging",
    .25,
    "leg",
    25
    )

naked = Armor(
    "Naked",
    "",
    0,
    "",
    0
    )

# NPC instances  
# name, health, greeting, weapon, friendly, pacifist                  
sean = NPC(
    "Sean",
    100,
    "Hello Traveller",
    longsword,
    True,
    False
    )
    
alex = NPC(
    "Alex",
    100,
    "I'm a butt",
    fists_of_fury,
    True,
    False
    )
    
nate = Merchant(
    "Nate",
    100,
    "See anything you like?",
    no_weapon,
    True,
    False,
    [longsword, greatsword], 
    alex
    )

# Room Instances
# welcome message, name, exits, items, npcs, secret
bedroom1 = Room(
    "The bedroom agoining the the antechamber was equally as large and lavish with many beuitiful works of art hanging from its walls",
    "Bedroom(1)",
    {},
    {},
    [],
    ""
    )

hallway = Room(
    "The hallway was also just as beutiful and lavish as the rest of the rooms had been, with huge windows alowing a flooding in of natural light.",
    "Hallway",
    {},
    {},
    [],
    ""
    )

antechamber = Room(
    "You walk into a large and brightly lit antechamber, filled with incredibly expensive looking decor adorning its interior",
    "Antechamber",
    {"east": bedroom1, "north": hallway},
    {},
    [],
    ""
    )

torture_chamber = Room(
    "WELCOME TO DEATH",
    "Torture Chamber",
    {},
    {},
    [],
    ""
    )

starting_room = Room(
    "You awake in what appears to be a dungeon", 
    "Starting Room",
    {"south": torture_chamber, "east": antechamber},
    {"Longsword": longsword, "Greatsword": greatsword, "Eye of Aganom": eye_of_aganom},
    [nate, alex], 
    "There are many secrets in this room"
    )
    
test_room = Room(
    "This is a test room",
    "Test Room",
    {"Starting Room": starting_room},
    {}, 
    [nate],
    ""
    )


# Menu Instances
inventory = Menu("----------INVENTORY---------")
equipment = Menu("----------EQUIPMENT---------")
merchant_inventory = Menu("----------INVENTORY---------")

# Top level stuff
UNDERLINES = "______________________" # 22
all_items = [butterfly, longsword, greatsword, no_weapon, sword, scythe, fists_of_fury, gnomes, your_hammer, eye_of_aganom, pendant, iron_helm, iron_chest, naked]
all_rooms = [torture_chamber, starting_room, test_room]
all_npcs  = [sean, alex, nate]


player = Player("Sean", 100, [], 60, longsword, {"head": naked, "chest": naked, "legs": naked})


game = Game(starting_room, all_rooms, all_items, all_npcs, player)
game.start()
