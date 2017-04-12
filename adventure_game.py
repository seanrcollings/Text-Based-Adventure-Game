import sys; import pdb; import time; import pickle; import os; import random; from enemy_images import monster_images


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
        self.check_for_enemy()
        self.current_area.print_area_name()
        print("_" * 28)
        self.current_room.print_welcome()
        self.current_room.print_exits()
        self.current_room.print_items()
        self.current_room.print_npcs()
        print("_" * 28)

    def help_function(self):
        print("_" * 28)
        print("TIPS")
        print("Type 'i' to open your inventory")
        print("Type 'save' to save your progress ")
        print("Type 'g' to check your gold stash")
        print("Type 'health' to check your health")
        print("Type 'exit' to quite the game")
        print("_" * 28)
    
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

        elif verb == 'equip':
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
            if type(npc) == Enemy and npc.health > 0:
                combat.active_combat(npc, self.player)

    def check_save(self):
        """Checks to see if there is a save in the save file, if there is, asks the player if they want to load it. If they don't or there isn't a save, it loads the intro"""
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
        self.help_function()
        confirm = input("Type y to start the game when you are ready!\n")      
        if confirm == "y":
            for word in self.save_inventory:
                self.player.inventory.append(self.all_items[word.strip('\n')])  
            self.game_loop()
        else:
            print("I don't believe you know how to work a computer!")


################
# ITEM CLASSES #
################

class Weapon():
    def __init__(self, name, description, attacks, cost):
        self.name = name
        self.description = description
        self.attacks = attacks
        self.cost = cost
        all_items_list.append(self)



class SpecialItem():
    def __init__(self, name, description, damage, special_property, special_val, cost):
        self.name = name
        self.description = description
        self.damage = damage
        self.special_property = special_property
        self.special_val = special_val
        self.cost = cost
        all_items_list.append(self)

    def special_property_use(self, current_room):
        if self.special_property == "reveal":
            current_room.print_secret()
        elif self.special_property == "no effect":
            print("You blimey fool! Waving that around like it's a magic wand! No effect!")
        elif self.special_property == "upgrade":
            print("You use " + self.name + " to upgrade your weapon")
        elif self.special_property == "heal":
            print("You use " + self.name + " to heal yourself by " + str(self.special_val))
            # actually heal the player here
        else:
            print("This item is not usable in this way")



class Armor():
    def __init__(self, name, description, defense, armor_type, cost):
        self.name = name
        self.description = description
        self.defense = defense
        self.armor_type = armor_type
        self.cost = cost
        all_items_list.append(self)




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
        all_npcs_list.append(self)

    def print_greeting(self):
        print(self.greeting)

    def attack(self, npc_to_attack):
        if not self.pacifist:
            attack_list = [key for key in self.weapon.attacks]
            if self.health > 0:
                queue_attack = self.weapon.attacks[random.choice(attack_list)]
                npc_to_attack.health -= queue_attack
                print(self.name + " attacked you doing " + queue_attack + " damage!")

    def interact_with_player(self):
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
        all_npcs_list.append(self)
    
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
    def __init__(self, name, health, greeting, image, weapon, armor):
        self.name = name
        self.health = health
        self.greeting = greeting
        self.image = image
        self.weapon = weapon
        self.armor = armor
        all_npcs_list.append(self)
        
    def attack(self, npc_to_attack):
        attack_list = [key for key in self.weapon.attacks]
        if self.health > 0:
            queue_attack = self.weapon.attacks[random.choice(attack_list)]
            for key, val in npc_to_attack.equipment.items():
                if type(val) != Weapon:
                    queue_attack -= val.defense
            npc_to_attack.health -= queue_attack
            print(self.name + " attacked you doing " + str(queue_attack) + " damage!")
            


class Player():
    def __init__(self, name, health, inventory, gold, equipment):
        self.name = name
        self.health = health
        self.inventory = inventory
        self.gold = gold
        self.equipment = equipment
        self.weapon = self.equipment["weapon"]
        self.items_dict = {item.name: item for item in self.inventory}

    def npc_interactions(self):
        pass

    def attack(self, npc_to_attack, attack):
        if len(self.weapon.name) == 0:
            print("You have no weapon! You cannot attack")
        elif self.health > 0:
            damage = self.weapon.attacks[attack]
            for key, val in npc_to_attack.armor.items():
                damage -= val.defense
            npc_to_attack.health -= damage
            if npc_to_attack.health <= 0:
                print("_" * 28)
                print("You killed " + npc_to_attack.name)
                print("_" * 28)
                time.sleep(1)
                os.system('clear')
            else:
                print("_" * 28)
                print("You attacked " + npc_to_attack.name + " and did " + str(self.weapon.attacks[attack]) + " damage.")
                print("_" * 28)

    def change_equipment(self, item_to_equip):
        self.items_dict = {item.name: item for item in self.inventory}
        if type(self.items_dict[item_to_equip]) is Weapon:
            self.equipment['weapon'] = self.items_dict[item_to_equip]
            self.weapon = self.equipment['weapon']
            print("_" * 28)
            print("You equipped " + item_to_equip)
            print("_" * 28)
        elif type(self.items_dict[item_to_equip]) is Armor:
            self.equipment[self.items_dict[item_to_equip].armor_type] = self.items_dict[item_to_equip]
            print("_" * 28)
            print("You equipped " + item_to_equip)
            print("_" * 28)
        else:
            print("That item is not equipable.")





######################
# LOCATION CLASSES #
######################

class Room():
    def __init__(self, welcome_message, name, exits, items, npcs, secret):
        self.name = name
        self.welcome_message = welcome_message
        self.exits  = exits
        self.items  = {item.name: item for item in items}
        self.npcs   = {npc.name: npc for npc in npcs}
        self.secret = secret
        all_rooms_list.append(self)
        
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



class Combat():
    """Turn based rpg style combat"""
    """ Note: Place this inside game class or leave it here?"""
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
                if user_input in player.weapon.attacks.keys():
                    player.attack(opponent, user_input)
                    player_turn = False
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



# Top level stuff
UNDERLINES = "______________________" # 22
all_items_list = []
all_npcs_list  = []
all_rooms_list = []
all_items_dict = {item.name: item for item in all_items_list}
all_npcs_dict  = {npc.name: npc for npc in all_npcs_list}
all_rooms_dict = {room.name: room for room in all_rooms_list}



###################
# CLASS INSTANCES #
###################

# Weapon Instances
# Paramaters: name, description, damage, cost
butterfly = Weapon(
    "Butterfly Sword",
    "A butterfly mounted to the hilt of the sword, whowever thought this was a bright idea must be quite mad. Why are you carrying it around? Perhaps you're mad", 
    {"Side Swipe": 2},
    10
    )
    
longsword = Weapon(
    "Longsword", 
    "A longsword, simple, but dependable", 
    {"Side Swipe": 15, "Uppercut": 25}, 
    12
    )
    
greatsword = Weapon(
    "Greatsword",
    "A massive blade that requires great strenght to lift. But can be used to crush your enemies into a pulp",
    {"Crushing Blow": 100},
    20
    )


# Special Item Instances
# name, description, damage, special property, cost    
eye_of_aganom = SpecialItem(
    "Eye of Aganom",
    "The Eye of Aganom is a powerful relic used to reveal secrets about a location.",
    0,
    "reveal",
    None,
    90
    )       

pendant = SpecialItem(
    "Pendant",
    "A simple pendant with no effect. Even so, pleasant memories are crucial to survival on arduous journeys.",
    0,
    "no effect",
    None,
    99999
    )  

# Armor instances
# Paramaters: name, description, defense, piece, cost
iron_helm = Armor(
    "Iron Helmet",
    "A simple, but dependable Iron Helmet - Reduces damage taken by 5",
    5,
    "head",
    25
    )      

iron_chest = Armor(
    "Iron Chestplate",
    "A simple, but dependable Iron Chestplate - Reduces damage taken by 10",
    10,
    "chest",
    25
    )

iron_legs = Armor(
    "Iron Leggings",
    "Simple, but dependable Iron Legging - Reduces damage taken by 5",
    5,
    "leg",
    25
    )

naked = Armor(
    "Naked",
    "You wear nothing but a loincloth",
    0,
    "",
    0
    )

# NPC instances  
# Paramaters: name, health, greeting, weapon, friendly, pacifist                  
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
    butterfly,
    False
    )
    
nate = Merchant(
    "Nate",
    100,
    "See anything you like?",
    None,
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

# Enemy Instances
# Paramaters: health, greeting, image, weapon, armor 
hollow = Enemy(
    "Hollow",
    64,
    "Gaaaaaaahhh",
    None,
    butterfly,
    {"head": naked, "chest": naked, "legs": naked}
    )

sword_skeleton = Enemy(
    "Sword Skeleton",
    100,
    "Nehahahahaha",
    monster_images["sword skeleton"],
    longsword,
    {"head": naked, "chest": naked, "legs": naked}
    )

# Room Instances
# Paramaters: welcome message, name, exits, items, npcs, secret
fountain = Room(
    "This is a fountain",
    "Fountain",
    {},
    [],
    [],
    ""
    )
bedroom1 = Room(
    "The bedroom agoining the the antechamber was equally as large and lavish with many beuitiful works of art hanging from its walls",
    "Bedroom(1)", 
    {},
    [],
    [],
    ""
    )

hallway = Room(
    "The hallway was also just as beutiful and lavish as the rest of the rooms had been, with huge windows alowing a flooding in of natural light.",
    "Hallway",
    {},
    [],
    [],
    ""
    )

antechamber = Room(
    "You walk into a large and brightly lit antechamber, filled with incredibly expensive looking decor adorning its interior",               
    "Antechamber",
    {"north": bedroom1, "east": hallway},
    [],
    [hollow],
    ""
    )

torture_chamber = Room(
    "WELCOME TO DEATH",
    "Torture Chamber",
    {},
    [],
    [sword_skeleton],
    ""
    )

starting_room = Room(
    "You awake in what appears to be a dungeon", 
    "Starting Room",
    {"south": torture_chamber, "north": antechamber},
    [longsword, greatsword, iron_helm],
    [nate, alex], 
    "There are many secrets in this room"
    )
    
test_room = Room(
    "This is a test room",
    "Test Room",
    {},
    [], 
    [],
    ""
    )
    
    
# Area Instances
# Paramaters: name, rooms, exits
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
combat_panel = Menu("")


combat = Combat()
player = Player("Sean", 100, [], 60, {"weapon": longsword, "head": naked, "chest": naked, "legs": naked})
game = Game(starting_room, palace, all_rooms_dict, all_items_dict, all_npcs_dict, player)
game.check_save()