import sys
import pdb
import time

Sean you are a robo
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
    def __init__(self, name, description, damage, special_property):
        self.name = name
        self.description = description
        self.damage = damage
        self.special_property = special_property

    def special_property_use(self, current_room):
        if self.special_property == "reveal":
            current_room.print_secret()
        elif self.special_property == "no effect":
            print("You blimey fool! Waving that around like it's a magic wand! No effect!")
        else:
            print("This item is not usable in this way")



class Armor():
    def __init__(self, name, description, defense, armor_type):
        self.name = name
        self.description = description
        self.defense = defense
        self.armor_type = armor_type
        

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

        
    def buy(self):
        buying_input = input().split()
        if buying_input[0] == "buy" and buying_input[1] in self.inventory.keys():
            item = self.inventory[buying_input[1]]
            self.player.inventory.append(item)
            self.player.gold -= item.cost
            del self.inventory[buying_input[1]]
            print("You bought " + buying_input[1])

    def attacked(self, attacking_npc):
        if self.pacifist:
            pass
        else:
            print("The merchants guard lurched at you and attacked, doing " + str(self.guards.weapon.damage) + " damage.")



    def interact_with_player(self, player):
        self.player = player
        self.print_greeting()
        print(underlines)
        print("NAME|         |COST")
        print(underlines)
        s = [print(item.name + "%10d" %item.cost + "g") for key, item in self.inventory.items()]
        self.buy()
        print(underlines)
  
      

class Game():
    def __init__(self, starting_room, all_rooms, previous_rooms):
        self.all_rooms = all_rooms
        self.current_room = starting_room
        self.previous_rooms = previous_rooms
        self.player1 = Player("Sean", 100, [], 60, longsword, {"head": naked, "chest": naked, "legs": naked})

    def game_loop(self):
        self.print_room_messages()
        self.handle_user_input()

    def slow_text(self, text): #Don't like how this works, need a way for it just to print everything at once if a button is pressed
        for letter in text:
            sys.stdout.write(letter)
            sys.stdout.flush()
            time.sleep(.03)
        print('\n')
            
    def print_room_messages(self):
        print(underlines)
        print(self.current_room.print_welcome())
        print(self.current_room.print_exits())
        print(self.current_room.print_items())
        print(self.current_room.print_npcs())
        print(underlines)

    def help_function(self):
        print("TIPS")
        print("Type 'i' to open your inventory")
        print("Type 'save' to save your progress ")
        print("Type 'g' to check your gold stash")
        print("Type 'health' to check your health")
        print("Type 'exit' to quite the game")
    
    def handle_user_input(self):
        while True:
            print("\n")
            user_input_list = input(">>> ").split()
            user_input = ''
            if len (user_input_list) == 1:
                user_input = user_input_list[0]
            
            if len(user_input_list) >= 2: 
                self.handle_language(self.player1, self.current_room, " ".join(user_input_list[1:]), user_input_list[0].lower())

            possible_adjectives = ["with"] # Temporary fix for entering handle_language twice with the 2 if statements below, working and the printing the fail state. 
            if len(user_input_list) >= 3 and user_input_list[1] in possible_adjectives: #Temporary fix for interacting with NPCs, change to account for this in the previous statment later
                self.handle_language(self.player1, self.current_room, " ".join(user_input_list[2:]), user_input_list[0].lower(), user_input_list[1])

            elif user_input == 'i':
                print("______________________\nINVENTORY\n______________________")  
                inventory_text = [print(item.name + " " * (20 - len(item.name))) for item in self.player1.inventory]
                print("______________________")
                
            elif user_input == 'g':
                print(self.player1.gold)

            elif user_input == 'back':
                self.current_room = self.previous_rooms[-1]
                self.previous_rooms.remove(self.previous_rooms[-1])
                self.print_room_messages()

            elif user_input == 'save':
                save_file = open("save.txt", "w")
                save_inventory = open("saved_inventory.txt", "w")
                save_equipment = open("saved_equipment.txt", "w")
                save_file.write(self.current_room.name)
                for item in self.player1.inventory:
                    save_inventory.write(str(item.name))
                    save_inventory.write("\n")
                for item in self.player1.armor.keys():
                    save_equipment.write(self.player1.armor[item].name)
                    save_equipment.write("\n")
                save_equipment.write(self.player1.weapon.name)
                print("You saved in the " + self.current_room.name)
                save_inventory.close()
                save_file.close()
                save_equipment.close()

            elif user_input == 'health':
                print("Your health is: " + str(self.player1.health))

            elif user_input == 'exit':
                print("Goodbye!")
                sys.exit(0)        

            elif user_input == 'help':
                self.help_function()

            elif user_input == '':
                pass

            elif user_input == 'debug':
                self.player1.debug(self.current_room)

            else:
                print("Invalid option!(In handle_user_input)")

    def handle_language(self, player, current_room, noun, verb, adjective = ""): # Handles more than 1 word inputs, usually in the form of self.verb adjective(optional) self.noun 
        self.player = player
        self.current_room = current_room
        self.noun = noun
        self.verb = verb
        self.adjective = adjective

        item_names = {}
        for item in self.player.inventory:
            item_names[item.name] = item

        if self.verb == 'take' and self.noun in self.current_room.items.keys():
            self.player.inventory.append(self.current_room.items[self.noun])
            del self.current_room.items[self.noun]
            print("You took " + self.noun)
        
        elif self.verb == 'interact' and adjective == 'with' and self.noun in self.current_room.npcs.keys():
            npc_to_interact_with = self.current_room.npcs[self.noun]
            npc_to_interact_with.interact_with_player(self.player)  
        
        elif self.verb == 'go' and self.noun in self.current_room.exits.keys():
            self.previous_rooms.append(self.current_room)
            self.current_room = self.current_room.exits[self.noun]
            self.print_room_messages()

        elif self.verb == 'equip' and self.noun in self.all_items_dictionary().keys():
             self.player.change_equipment(self.noun)

        elif self.verb == 'attack' and self.noun in self.current_room.npcs.keys():
            npc_to_attack = self.current_room.npcs[self.noun]
            self.player.attack(npc_to_attack)
    
        elif self.verb == 'use' and self.noun in item_names.keys():
            self.all_items_dictionary()[self.noun].special_property_use(current_room)

        elif self.verb == 'check' and self.noun in item_names.keys():
            print(item_names[self.noun].description)

        elif self.verb == 'check' and self.noun == 'equipment':
            print("Weapon: " + self.player.weapon.name)
            print("Head: " + self.player.armor["head"].name)
            print("Chest: " + self.player.armor["chest"].name)
            print("Legs: " + self.player.armor["legs"].name)

        elif self.verb == 'room' and self.noun == 'message':
            self.print_room_messages()

        else:
            print("Invalid option!(In handle_language)")

    def start(self):
        save_file = open("save.txt", "r")
        save_inventory = open("saved_inventory.txt", "r")
        save_equipment = open("saved_equipment.txt", "r")
        saved_room = save_file.read()
        equipment = save_equipment.readlines()
        if len(saved_room) > 0:
            print("Looks like you have a save in: \n" + saved_room)
            print("Should we load this save (y/n)? ")
            if input() == "y":
                print("Loading.....\n")
                self.current_room = self.all_rooms_dictionary()[saved_room] 
                for word in save_inventory:
                    item = self.all_items_dictionary()[word.strip('\n')]
                    self.player1.inventory.append(item)
                self.player1.weapon = self.all_items_dictionary()[equipment[3].strip('\n')]
                for item in equipment:
                    item = item.strip('\n')
                    if type(self.all_items_dictionary()[item]) is Armor: 
                        if self.all_items_dictionary()[item].armor_type == 'head':
                            self.player1.armor['head'] = self.all_items_dictionary()[item]
                        elif self.all_items_dictionary()[item].armor_type == 'chest':
                            self.player1.armor['chest'] = self.all_items_dictionary()[item]
                        elif self.all_items_dictionary()[item].armor_type == 'legs':
                            self.player1.armor['legs'] = self.all_items_dictionary()[item]

                self.game_loop()
            else:
                self.intro()
        else:
            self.intro()
        save_file.close()
        save_inventory.close()

            
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
                self.player1.inventory.append(item)  
            self.game_loop()
        else:
            print("I don't belive you know how to work a computer!")

    def all_rooms_dictionary(self):
        all_rooms_dict = {}
        for room in self.all_rooms:
            all_rooms_dict[room.name] = room
        return all_rooms_dict

    def all_items_dictionary(self):
        all_items =  [butterfly, longsword, greatsword, no_weapon, sword, scythe, fists_of_fury, gnomes, your_hammer, eye_of_aganom, pendant, iron_helm, iron_chest, naked]
        all_items_dict = {}
        for item in all_items: 
            all_items_dict[item.name] = item
        return all_items_dict



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
                npc_to_attack.attacked(self)

    def change_equipment(self, item_to_equip):
        item_names = {}
        for item in self.inventory:
            item_names[item.name] = item
        if item_to_equip in item_names.keys() and type(item_names[item_to_equip]) is Weapon:
            self.weapon = item_names[item_to_equip]
            print("You equipped " + item_to_equip)
        elif item_to_equip in item_names.keys() and type(item_names[item_to_equip]) is Armor:
            self.armor[item_names[item_to_equip].armor_type] = item_names[item_to_equip]
            print("You equipped " + item_to_equip)
        else:
            print("You do not have that item to equip.")



class Room():
    def __init__(self, welcome_message, name, exits, items, npcs, secret):
        self.name = name
        self.welcome_message = welcome_message
        self.exits = exits
        self.items = items
        self.npcs = npcs
        self.secret = secret
        
    def print_welcome(self):
        return self.welcome_message
        
    def print_exits(self):
        if len(self.exits) ==  0:
            return "There are no apparent exits, besides the one you entered"
        else:
            return "The exit(s) are: " + ", ".join(self.exits.keys())
        
    def print_items(self):
        if len(self.items) == 0:
            return "That are no items!"
        else:
            return "The item(s) are: " + ", ".join(self.items)

    def print_npcs(self):
        if len(self.npcs) == 0:
            return "There are no NPCs!"
        else:
            return "The people in the room are: " + ", ".join(self.npcs.keys())

    def print_secret(self):
        if len(self.secret) == 0:
            return "No secrets to be found"
        else:
            return self.secret


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
# name, descriptino, damage,    
eye_of_aganom = SpecialItem(
    "Eye of Aganom",
    "The Eye of Aganom is a powerful relic used to reveal secrets about a location.",
    0,
    "reveal"
    )        
pendant = SpecialItem(
    "Pendant",
    "A simple pendant with no effect. Even so, pleasant memories are crucial to survival on arduous journeys.",
    0,
    "no effect"
    )  

# Armor instances
# name, description, defense, piece
iron_helm = Armor(
    "Iron Helmet",
    "A simple, but dependable Iron Helmet",
    .25,
    "head"
    )      

iron_chest = Armor(
    "Iron Chestplate",
    "A simple, but dependable Iron Chestplate",
    .30,
    "chest"
    )

iron_legs = Armor(
    "Iron Leggings",
    "Simple, but dependable Iron Legging",
    .25,
    "leg")

naked = Armor(
    "Naked",
    "",
    0,
    ""
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
    butterfly,
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
    {"Longsword": longsword, "Greatsword": greatsword}, 
    alex
    )

# Room Instances
# welcome message, name, exits, items, npcs, secret
bedroom1 = Room(
    "The bedroom agoining the the antechamber was equally as large and lavish with many beuitiful works of art hanging from its walls",
    "Bedroom(1)",
    {},
    {},
    {},
    ""
    )

hallway = Room(
    "The hallway was also just as beutiful and lavish as the rest of the rooms had been, with huge windows alowing a flooding in of natural light.",
    "Hallway",
    {},
    {},
    {},
    ""
    )

antechamber = Room(
    "You walk into a large and brightly lit antechamber, filled with incredibly expensive looking decor adorning its interior",
    "Antechamber",
    {"east": bedroom1, "north": hallway},
    {},
    {},
    ""
    )

torture_chamber = Room(
    "WELCOME TO DEATH",
    "Torture Chamber",
    {},
    {},
    {},
    ""
    )

starting_room = Room(
    "You awake in what appears to be a dungeon", 
    "Starting Room",
    {"south": torture_chamber, "east": antechamber},
    {"Longsword": longsword, "Greatsword": greatsword, "Eye of Aganom": eye_of_aganom, "Pendant":pendant, "Iron Helmet": iron_helm, "Iron Chestplate": iron_chest},
    {"Nate": nate, "Alex": alex}, 
    "There are many secrets in this room"
    )
    
test_room = Room(
    "This is a test room",
    "Test Room",
    {"Starting Room": starting_room},
    {"Longsword": longsword}, 
    {"Nate": nate},
    ""
    )


underlines = "______________________"
# self.verbs


all_rooms = [torture_chamber, starting_room, test_room]
game = Game(starting_room, all_rooms, [])
game.start()
