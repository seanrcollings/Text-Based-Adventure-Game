############
#TO DO LIST#
############

# Incorperate verbs(Possibly with a verb class?)
# ??????
# Profit
import sys
 

 
("""
 _                                                                                                                  _ 
| |                                                                                                                | |
\_/  _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____   \_/
 _   \____\\____\\____\\____\\____\\____\\____\\____\\____\\____\\____\\____\\____\\____\\____\\____\\____\\____\   _ 
/ \                                                                                                                / \
|_|     _      _____ _     ____  ____  _      _____   _____  ____    _     ___  _   _____ ____  _      _____ _     |_|
| |    / \  /|/  __// \   /   _\/  _ \/ \__/|/  __/  /__ __\/  _ \  / \__/|\  \//  /  __//  _ \/ \__/|/  __// \    | |
\_/    | |  |||  \  | |   |  /  | / \|| |\/|||  \      / \  | / \|  | |\/|| \  /   | |  _| / \|| |\/|||  \  | |    \_/
 _     | |/\|||  /_ | |_/\|  \__| \_/|| |  |||  /_     | |  | \_/|  | |  || / /    | |_//| |-||| |  |||  /_ \_/     _ 
/ \    \_/  \|\____\\____/\____/\____/\_/  \|\____\    \_/  \____/  \_/  \|/_/     \____\\_/ \|\_/  \|\____\(_)    / \
|_|                                                                                                                |_|
| |                                                                                                                | |
\_/  _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____   \_/
 _   \____\\____\\____\\____\\____\\____\\____\\____\\____\\____\\____\\____\\____\\____\\____\\____\\____\\____\   _ 
/ \                                                                                                                / \
|_|                                                                                                                |_|""")     


class Weapon():
    def __init__(self, name, description, damage, cost):
        self.name = name
        self.description = description
        self.damage = damage
        self.cost = cost
       

    """def use_wpn_art(self, npc_to_attack):
        self.damage *= 2"""  


class Item():
    def __init__(self, name, description, damage, special_property = 0):
        self.name = name
        self.description = description
        self.damage = damage
        self.special_property = special_property

def special_property(self):
    pass



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
        if self.pacifist:
            pass
        else:
            npc_to_attack.health -= self.weapon.damage 
        
    def attacked(self, attacking_npc):
        self.health -= attacking_npc.weapon.damage
        if self.pacifist:
            pass
        else:
            attacking_npc.health -= self.weapon.damage

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

        
    def buy(self, player):
        self.player = player
        buying_input = input().split()
        if buying_input[0] == "buy" and buying_input[1] in self.inventory.keys():
            item = self.inventory[buying_input[1]]
            self.player.inventory.append(item)
            self.player.gold -= item.cost
            del self.inventory[buying_input[1]]
            

    def attacked(self, attacking_npc):
        if self.pacifist:
            pass
        
        else:
            attacking_npc.health -= self.guards.weapon.damage
            print("The merchants guard lurched at you and attacked, doing " + str(self.guards.weapon.damage) + " damage.")
    
    def interact_with_player(self, player):
        self.player = player
        self.print_greeting()
        print("NAME***********COST")
        for key, item in self.inventory.items():
            spaces = " " * (15 - len(item.name))
            print(item.name + spaces + str(item.cost) + "g")
        self.buy(self.player)
        


class Game():
    def __init__(self, starting_room, all_rooms):
        self.all_rooms = all_rooms
        self.current_room = starting_room
        self.player1 = Player("Sean", 100, [], 60, longsword)

    def game_loop(self):
        self.print_room_messages()
        self.handle_user_input()
            
    def print_room_messages(self):
        print(underlines)
        self.current_room.print_welcome()
        self.current_room.print_exits()
        self.current_room.print_items()
        self.current_room.print_npcs()
        print(underlines)


    def help_function(self):
        print("TIPS")
        print("Type 'i' to open your inventory")
        print("Type 'save' to save your progress ")
        print("Type 'g' to check your gold stash")
        print("Type 'health' to check your health")
        print("Type 'exit' to quite the game")
    
    #TODO: Make these more like a verb set(for now at least, hopefully have a another way at some point)    
    def handle_user_input(self):
        while True:
            user_input_list = input().split()
            
            user_input = ''
            if len(user_input_list) > 0:
                user_input = user_input_list[0]
            
            # Ways for the player to interact with/ move in  their surroundings

            if len(user_input_list) >= 2 and user_input_list[0] == "interact" and user_input_list[1] == "with":
                npc_to_interact_with = self.current_room.npcs[user_input_list[2]]
                # TODO: what if the NPC doesn't exist?
                npc_to_interact_with.interact_with_player(self.player1)

            elif len(user_input_list) >= 2 and user_input_list[0] == "attack" and user_input_list[1] in self.current_room.npcs.keys():
                npc_to_attack = self.current_room.npcs[user_input_list[1]]
                self.player1.attack(npc_to_attack)
                
            elif user_input in self.current_room.exits.keys():
                self.current_room = self.current_room.exits[user_input]
                self.print_room_messages()

            elif len(user_input_list) >= 2 and user_input_list[0] == "take" and user_input_list[1] in self.current_room.weapons.keys().split()[1]:
                print("You took "+ self.current_room.weapons[user_input_list[1]].name)
                self.player1.inventory.append(self.current_room.weapons[user_input_list[1]])

            elif len(user_input_list) >= 2 and user_input_list[0] == "take" and user_input_list[1] in self.current_room.items.keys():
                print("You took "+ self.current_room.items[user_input_list[1]].name)
                self.player1.inventory.append(self.current_room.items[user_input_list[1]])

            elif len(user_input_list) >= 2 and user_input_list[0] == "equip" and user_input_list[1] in self.all_weapons_dictionary().keys():
                self.player1.change_equipment(user_input_list[1])

            # Informational statements, outputs information

            elif user_input == "i":
                print("______________________\nINVENTORY\n______________________")    
                for item in self.player1.inventory:
                    spaces = " " * (20 - len(item.name))
                    print(item.name + spaces)
                print("______________________")
            
            elif user_input == "g":
                print(self.player1.gold)

            elif user_input == "save":
                save_file = open("save.txt", "w")
                save_inventory = open("saved_inventory.txt", "w")
                save_file.write(self.current_room.name)
                for item in self.player1.inventory:
                    save_inventory.write(str(item.name))
                    save_inventory.write("\n")
                print("You saved in the " + self.current_room.name)
                save_inventory.close()
                save_file.close()
            
            elif user_input == "health":
                print("Your health is: " + self.player1.health)

            elif user_input == 'exit':
                print("Goodbye!")
                sys.exit(0)        

            elif user_input == "help":
                self.help_function()

            elif user_input == '':
                pass

            elif user_input == "debug":
                self.player1.debug(self.current_room)

            else:
                print("Invalid option!")
               
    def start(self):
        save_file = open("save.txt", "r")
        save_inventory = open("saved_inventory.txt", "r")
        saved_room = save_file.read()
        if len(saved_room) > 0:
            print("Looks like you have a save in: \n" + saved_room)
            print("Should we load this save (y/n)? ")
            if input() == "y":
                print("Loading.....\n")
                self.current_room = self.all_rooms_dictionary()[saved_room] 
                for word in save_inventory:
                    item = self.all_weapons_dictionary()[word.strip('\n')]
                    self.player1.inventory.append(item)  
                self.game_loop()
            else:
                self.intro()
        else:
            self.intro()
        save_file.close()
        save_inventory.close()
            
    def intro(self, save_inventory=['Longsword']):
        self.save_inventory = save_inventory   
        print("Thanks for playing my simple little game!!!!")
        print("Just popping in before the game to give a couple tips:")
        print("1. Press i will allow you to view your inventory")
        print("2. Typing save will allow you to save your game")
        print("3. You can acess the help at any time by typing help")
        confirm = input("Type y to start the game when you are ready!\n")
            
        if confirm == "y":
            for word in self.save_inventory:
                item = self.all_weapons_dictionary()[word.strip('\n')]
                self.player1.inventory.append(item)  
            self.game_loop()
        else:
            print("I don't belive you know how to work a computer!")

    def all_rooms_dictionary(self):
        all_rooms_dict = {}
        for room in self.all_rooms:
            all_rooms_dict[room.name] = room
        return all_rooms_dict

    def all_weapons_dictionary(self):
        all_weapons =  [butterfly, longsword, greatsword, no_weapon, sword, scythe, fists_of_fury, gnomes, your_hammer]
        all_weapons_dict = {}
        for item in all_weapons: 
            all_weapons_dict[item.name] = item
        return all_weapons_dict

    def all_items_dictionary(self):
        all_items = [eye_of_aganom]
        all_items_dict = {}
        for item in all_items:
            all_items_dict[item.name] = item
        return all_items_dict



class Player():
    def __init__(self, name, health, inventory, gold, equipped):
        self.name = name
        self.health = health
        self.inventory = inventory
        self.gold = gold
        self.equipped = equipped

    def npc_interactions(self):
        pass

    def attack(self, npc_to_attack):
        self.npc_to_attack = npc_to_attack
        if len(self.equipped.name) == 0:
            print("You have no weapon! You cannot attack")
        else:
            self.npc_to_attack.health -= self.equipped.damage
            print("You attacked " + npc_to_attack.name + " and did " + str(self.equipped.damage) + " damage.")
            npc_to_attack.attacked(self)

    def debug(self, current_room):
        self.current_room = current_room
        print("What would you like to know about the current room: " + self.current_room.name + "?")
        user_input = input()
        if user_input == "health":
            for key, npc in self.current_room.npcs:
                print(npc.name + ": Health: " + npc.health)

    def change_equipment(self, user_input):
        self.user_input = user_input
        item_names = {}
        for item in self.inventory:
            item_names[item.name] = item
        if user_input in item_names:
            self.equipped = item_names[user_input]
            print("You equipped " + user_input)
        else:
            print("You do not have that item to equip.")



class Room():
    def __init__(self, welcome_message, name, exits, weapons, npcs, items):
        self.name = name
        self.welcome_message = welcome_message
        self.exits = exits
        self.weapons = weapons
        self.npcs = npcs
        self.items = items 
        
    def print_welcome(self):
        print(self.welcome_message)
        
    def print_exits(self):
        if len(self.exits) ==  0:
            print("There are no exits!")
        else:
            print("The exit(s) are: " + ", ".join(self.exits.keys()))
        
    def print_items(self):
        if len(self.items) and len(self.weapons) == 0:
            print("That are no items!")
        else:
            print("The item(s) are: " + ", ".join(self.items.keys()) + ", " + ", ".join(self.weapons.keys()))

    def print_npcs(self):
        if len(self.npcs) == 0:
            print("There are no NPCs!")
        else:
            print("The people in the room are: " + ", ".join(self.npcs.keys()))



###################
# CLASS INSTANCES #
###################

# Weapon Instances
butterfly = Weapon("Butterfly Sword","A butterfly mounted to the hilt of the sword, whowever thought this was a bright idea must be quite mad. Why are you carrying it around? Maybe you're mad" , 2, 10)
longsword = Weapon("Longsword", "A longsword, simple, but dependable", 45, 12)
greatsword = Weapon("Greatsword","A massive blade that requires great strenght to lift. But can be used to crush your enemies into a pulp", 89, 20)
no_weapon = Weapon("No Weapon", "Does not possess a weapon. Does not belive in such tom foolery" , 0, 0)

sword = Weapon("Sword","A plain sword, made of steel in a human forge. A decent overall weapon.", 40, 10)
scythe = Weapon("Scythe","A farming tool, sharpened to extreme measures. Useful for trapping an enemy's weapon.",30, 11)
fists_of_fury = Weapon("Fists of Fury", "LISTEN UP, YOU PANSY. USE YOUR FISTS. PUNCH THEM INTO SUBMISSION!!!", 9001, 17)
gnomes = Weapon("Infinite throwing gnomes","You're a horrible person if you use this", 100, 10)
your_hammer = Weapon("Your pitiful hammer","You can't do anything with this, no wonder the ladies laugh at you.", -5, 5)

# Item Instances
eye_of_aganom = Item("Eye Of Aganom", "The Eye of Aganom is a powerful relic used to reveal secrets about a location.", 0, "reveal")        
pendant = Item("Pendant", "A simple pendant with no effect. Even so, pleasant memories are crucial to survival on arduous journeys." , 0, "no effect")

# NPC instances                    
sean = NPC("Sean", 100, "Hello Traveller", longsword, True, False)
alex = NPC("Alex", 100, "I'm a butt", butterfly, True, False)
nate_inven = {"Longsword": longsword, "Greatsword": greatsword}
nate = Merchant("Nate", 100, "See anything you like?", no_weapon, True, False, nate_inven, alex)

# Room Instances
torture_chamber = Room("WELCOME TO DEATH", "Torture Chamber", {}, {}, {}, {})
starting_room = Room("You awake in what appears to be a dungeon", "Starting Room", {"south": torture_chamber}, {"Longsword": longsword, "Greatsword": greatsword}, {"Nate": nate, "Alex": alex}, {"Eye Of Aganom": eye_of_aganom, "Pendant": pendant})
test_room = Room("This is a test room", "Test Room", {"Starting Room": starting_room}, {"Longsword": longsword}, {"Nate": nate}, {"Eye Of Aganom": eye_of_aganom})

underlines = "______________________"
# Verbs



all_rooms = [torture_chamber, starting_room, test_room]
game = Game(starting_room, all_rooms)
game.start()
