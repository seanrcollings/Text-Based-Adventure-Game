import sys; import pdb; import time; import pickle


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
        elif self.special_property == "upgrade":
            print("You use " + self.name + " to upgrade your weapon")
        else:
            print("This item is not usable in this way")



class Armor():
    def __init__(self, name, description, defense, armor_type, cost):
        self.name = name
        self.description = description
        self.defense = defense
        self.armor_type = armor_type
        self.cost = cost



######################
# CLASSES FOR PEOPLE #
######################

class NPC():
    def __init__(self, name, health, greeting, weapon, pacifist):
        self.name = name
        self.health = health
        self.greeting = greeting
        self.weapon = weapon
        self.pacifist = pacifist

    def print_greeting(self):
        print(self.greeting)

    def attack(self, npc_to_attack):
        if not self.pacifist:
            print(self.name + "attack you doing " + str(self.weapon.damage) + " damage!")
            npc_to_attack.health -= self.weapon.damage

    def interact_with_player():
        pass



class Merchant(NPC):
    def __init__(self, name, health, greeting, weapon, pacifist, inventory, guards):
        self.name = name
        self.health = health
        self.greeting = greeting
        self.weapon = weapon
        self.pacifist = pacifist
        self.inventory = inventory
        self.guards = guards

    
    def buy(self, player):
        """Changed merchant inventory from a dictionary to a list, fix it accordingly"""
        self.inventory = {item.name: item for item in self.inventory}
        while True:
            buying_input = input('>>> ').split()
            verb = buying_input[0]
            noun = " ".join(buying_input[1:])
            if len(buying_input) != 2:
                print("In order to buy, say 'buy (item)'")
                print("In order to sell, say 'sell (item)'")
            elif verb == "buy" and noun in self.inventory:
                item = self.inventory[noun]
                player.inventory.append(item)
                player.gold -= item.cost
                del self.inventory[noun]
                print("You bought " + noun)
                break
            elif verb == "sell" and noun in player.items_dictionary().keys():
                player.inventory.remove(player.items_dictionary[noun])
                player.gold += player.items_dictionary[noun].cost
                print("You sold " + noun)
                break
            else:
                print("Invalid input.\n In order to buy, say 'buy (item)'\n In order to sell, say 'sell (item)'")

    def attack(self, attacking_npc):
        if not self.pacifist:
            self.guards.attack(attacking_npc)

    def interact_with_player(self, player):
        self.print_greeting()
        merchant_inventory.print_menu(self.inventory)
        self.buy(player)



class Enemy():
    def __init__(self, name, health, greeting, weapon, armor):
        self.name = name
        self.health = health
        self.greeting = greeting
        self.weapon = weapon
        self.armor = armor
        
    def attack(self, npc_to_attack):
        npc_to_attack.health -= self.weapon.damage
        print(self.name + " attacked you doing " + str(self.weapon.damage) + " damage!")
        npc_to_attack.attack(self)


class Player():
    def __init__(self, name, health, inventory, gold, equipment):
        self.name = name
        self.health = health
        self.inventory = inventory
        self.gold = gold
        self.equipment = equipment
        self.weapon = self.equipment["weapon"]
        self.items_dict = {item.name: item for item in inventory}

    def npc_interactions(self):
        pass

    def attack(self, npc_to_attack):
        if len(self.weapon.name) == 0:
            print("You have no weapon! You cannot attack")
        else:
            npc_to_attack.health -= self.weapon.damage
            if npc_to_attack.health <= 0:
                print("You killed " + npc_to_attack.name)
            else:
                print("You attacked " + npc_to_attack.name + " and did " + str(self.weapon.damage) + " damage.")
                npc_to_attack.attack(self)

    def change_equipment(self, item_to_equip):
        if type(self.items_dict[item_to_equip]) is Weapon:
            self.equipment["weapon"] = self.items_dict[item_to_equip]
            print("You equipped " + item_to_equip)
        elif type(self.items_dict[item_to_equip]) is Armor:
            self.equipment[self.items_dict[item_to_equip].armor_type] = self.items_dict[item_to_equip]
            print("You equipped " + item_to_equip)
        else:
            print("That item is not equipable.")



class Game():
    def __init__(self, starting_room, starting_area, all_rooms, all_items, all_npcs, player):
        """Main part of the game, handles primarily user input and it's interaction with the game world"""
        """Note: all_rooms, all_items, all_npcs have now been changed to dictionaries."""
        self.current_room = starting_room
        self.current_area = starting_area
        self.previous_rooms = []
        self.all_rooms = all_rooms
        self.all_items = all_items
        self.all_npcs = all_npcs
        self.player = player

    def game_loop(self):
        self.print_room_messages()
        self.handle_user_input()

    def slow_text(self, text): 
        """"Don't like how this works, need a way for it just to print everything at once if a button is pressed (Multi Threading?)"""
        for letter in text:
            sys.stdout.write(letter)
            sys.stdout.flush()
            time.sleep(.03)
        print('\n')

    def print_room_messages(self):
        self.current_area.print_area_name()
        print("_" * 28)
        self.current_room.print_welcome()
        self.current_room.print_exits()
        self.current_room.print_items()
        self.current_room.print_npcs()
        print("_" * 28)
        self.check_for_enemy()

    def help_function(self):
        print("TIPS")
        print("Type 'i' to open your inventory")
        print("Type 'save' to save your progress ")
        print("Type 'g' to check your gold stash")
        print("Type 'health' to check your health")
        print("Type 'exit' to quite the game")
    
    def handle_user_input(self):
        possible_adjectives = ["with"] # Temporary fix for entering handle_language twice with the 2 if statements below, working and the printing the fail state. 
        while self.player.health > 0:
            print("\n")
            user_input_list = input(">>> ").split()
            user_input = ''
            if len(user_input_list) == 1:
                user_input = user_input_list[0]
            
            elif len(user_input_list) >= 2 and user_input_list[1] not in possible_adjectives:
                self.handle_language(" ".join(user_input_list[1:]), user_input_list[0].lower())
        
            elif len(user_input_list) >= 3 and user_input_list[1] in possible_adjectives: # Temporary fix for interacting with NPCs, change to account for this in the previous statment later
                self.handle_language(" ".join(user_input_list[2:]), user_input_list[0].lower(), user_input_list[1])

            if user_input == 'i': # prints player inventory 
                inventory.print_menu(self.player.inventory)                                                

            elif user_input == 'g':
                print("You have: " + str(self.player.gold) + "gold.")

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
        """Handle more than 1 word inputs, usually in the form of verb adjective(optional) noun"""

        if verb == 'take' and noun in self.current_room.items.keys():
            self.player.inventory.append(self.current_room.items[noun])
            print("You took " + noun)
            print(self.player.items_dict)
        
        elif verb == 'interact' and adjective == 'with' and noun in self.current_room.npcs.keys():
            self.all_npcs[noun].interact_with_player(self.player)
        
        elif verb == 'go' and noun in self.current_room.exits.keys():
            self.previous_rooms.append(self.current_room)
            self.current_room = self.current_room.exits[noun]
            self.print_room_messages()

        elif verb == 'equip' and noun in self.player.items_dict.keys():
             self.player.change_equipment(noun)

        elif verb == 'attack' and noun in self.current_room.npcs.keys():
            self.player.attack(self.current_room.npcs[noun])
    
        elif verb == 'use' and noun in self.player.items_dict.keys():
            self.player.items_dict[noun].special_property_use(self.current_room)

        elif verb == 'check' and noun in self.player.items_dict:
            print(self.player.items_dict[noun].description)

        elif verb == 'check' and noun == 'equipment':
            equipment.print_menu(self.player.equipment)

        elif verb == 'room' and noun == 'message':
            self.print_room_messages()

        else:
            print("Invalid option!(In handle_language)")


    def check_for_enemy(self):
        for name, npc in self.current_room.npcs.items():
            if type(npc) == Enemy:
                npc.attack(self.player)


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

            
    def intro(self, save_inventory = []):
        self.save_inventory = save_inventory   
        print("TIPS")
        print("1. Press i will allow you to view your inventory")
        print("2. Typing save will allow you to save your game")
        print("3. You can acess the help at any time by typing help")
        confirm = input("Type y to start the game when you are ready!\n")      
        if confirm == "y":
            for word in self.save_inventory:
                self.player.inventory.append(self.all_items[word.strip('\n')])  
            self.game_loop()
        else:
            print("I don't believe you know how to work a computer!")



class Room():
    def __init__(self, welcome_message, name, exits, items, npcs, secret):
        self.name = name
        self.welcome_message = welcome_message
        self.exits  = {room.name: room for room in exits}
        self.items  = {item.name: item for item in items}
        self.npcs   = {npc.name: npc for npc in npcs}
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
            print("The people in the room are: " + ", ".join(self.npcs.keys()))

    def print_secret(self):
        if len(self.secret) == 0:
            print("No secrets to be found")
        else:
            print(self.secret)



class Area():
    def __init__(self, name, rooms, exits):
        self.name = name
        self.rooms = rooms
        self.exits = exits

    def print_area_name(self):
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
            for key, val in menu_components.items():
                print(val.name + " " * (26 - len(val.name + str(val.cost))) + str(val.cost) + "g |")
            print("_" * 28)


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
    .05,
    "head",
    25
    )      

iron_chest = Armor(
    "Iron Chestplate",
    "A simple, but dependable Iron Chestplate",
    .10,
    "chest",
    25
    )

iron_legs = Armor(
    "Iron Leggings",
    "Simple, but dependable Iron Legging",
    .05,
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
    False
    )
    
alex = NPC(
    "Alex",
    100,
    "I'm a butt",
    fists_of_fury,
    False
    )
    
nate = Merchant(
    "Nate",
    100,
    "See anything you like?",
    no_weapon,
    False,
    [longsword, greatsword],
    alex
    )
    
tanner = NPC(
    "Tanner",
    2,
    "Uneducated manatees mating :)",
    butterfly,
    False,
    )

oscar = NPC(
    "Oscar",
    1,
    "Thou who art undead art chosen. And in thine exedous from the Undead Asylum, make pilgrimige to the land of the ancient lords. If thou ringest the bells of awakening, the fate of the undead thou shalt know.",
    longsword,
    True,
    )

hollow = Enemy(
    "Hollow",
    64,
    "Gaaaaaaahhh",
    butterfly,
    {"head": naked, "chest": naked, "legs": naked}
    )

# Room Instances
# welcome message, name, exits, items, npcs, secret
fountain = Room(
    "This is a fountain",
    "Fountain",
    [],
    {},
    [],
    ""
    )
bedroom1 = Room(
    "The bedroom agoining the the antechamber was equally as large and lavish with many beuitiful works of art hanging from its walls",
    "Bedroom(1)", 
    [],
    [],
    [],
    ""
    )

hallway = Room(
    "The hallway was also just as beutiful and lavish as the rest of the rooms had been, with huge windows alowing a flooding in of natural light.",
    "Hallway",
    [],
    [],
    [],
    ""
    )

antechamber = Room(
    "You walk into a large and brightly lit antechamber, filled with incredibly expensive looking decor adorning its interior",               
    "Antechamber",
    [bedroom1, hallway],
    [],
    [hollow],
    ""
    )

torture_chamber = Room(
    "WELCOME TO DEATH",
    "Torture Chamber",
    [],
    [],
    [],
    ""
    )

starting_room = Room(
    "You awake in what appears to be a dungeon", 
    "Starting Room",
    [torture_chamber, antechamber],
    [longsword],
    [nate, alex], 
    "There are many secrets in this room"
    )
    
test_room = Room(
    "This is a test room",
    "Test Room",
    [starting_room],
    [], 
    [],
    ""
    )
    
    
# Area Instances
# name, rooms, exits
gardens = Area(
    "Gardens",
    [fountain],
    {}
    )
    
palace = Area(
    "Palace of Dreams",
    [starting_room, torture_chamber, antechamber, hallway, bedroom1],
    {"Fountain": [gardens, fountain]}
    )


# Menu Instances
inventory = Menu("----------INVENTORY---------")
equipment = Menu("----------EQUIPMENT---------")
merchant_inventory = Menu("----------INVENTORY---------")

# Top level stuff
UNDERLINES = "______________________" # 22
all_items_list = [butterfly, longsword, greatsword, no_weapon, sword, scythe, fists_of_fury, gnomes, your_hammer, eye_of_aganom, pendant, iron_helm, iron_chest,naked]
all_rooms_list = [torture_chamber, starting_room, test_room]
all_npcs_list  = [sean, alex, nate, tanner, oscar, hollow]
all_items_dict = {item.name: item for item in all_items_list}
all_rooms_dict = {room.name: room for room in all_rooms_list}
all_npcs_dict  = {npc.name: npc for npc in all_npcs_list}


player = Player("Sean", 100, [], 60, {"weapon": longsword, "head": naked, "chest": naked, "legs": naked})
game = Game(starting_room, palace, all_rooms_dict, all_items_dict, all_npcs_dict, player)
game.start()
