#Corban Bindrup
#Sean Collins
#Mason Davis

import sys; import pdb; import time; import os; import random; from title import title_text # Imports all of the Stuff and Things


class Game(): 
    """The game class dictates the interactions between the other objects"""
    def __init__(self, player):
        self.player = player
        self.scripts = {'window' : self.outro}
    
    def game_loop(self):
        self.player.print_room_menu()
        self.handle_user_input()
    # deals with the users input and puts it to use
    def handle_user_input(self):
        """The main portion of the game class, takes the user input then reacts accordingly"""
        while self.player.health > 0:
            
            if self.player.current_room.name in self.scripts.keys():
                self.scripts[self.player.current_room.name]()

            user_input_list = input('>>> ').lower().split()
            user_input = ''
            noun = ''
            verb = ''
            
            if len(user_input_list) >= 2:
                verb = user_input_list[0]
                noun = ' '.join(user_input_list[1:])
            else:
                user_input = ' '.join(user_input_list[0:])
            
            if user_input == 'back': # Allows the user to move back in rooms
                self.player.go_back()
                
            elif user_input == 'i' or user_input == 'inventory':
                print("_" * 28)
                print("INVENTORY")
                print("_" * 28)
                print("NAME--------------DURABILITY")
                for item in self.player.inventory:
                    print(item.name + " " * (26 - len(item.name + str(item.durability))) + str(item.durability) + " |")
                print("_" * 28)
                
            elif user_input == 'help':
                self.help_info()
            
            elif user_input == 'cheat':
                self.player.health += 500
                self.player.weapon = easter_egg
                
            # The exit command to leave the game.
            elif user_input == 'quit' or user_input == 'exit' or user_input == 'rage': 
                # prints the Exit message
                print("You Lose, Goodbye!")
                sys.exit(0)

            elif user_input == '' and verb == '':
                pass

            elif verb == 'go' and noun in self.player.current_room.exits.keys(): # Allows you to move between rooms
                self.player.change_rooms(self.player.current_room.exits[noun])

            elif verb == 'take' and noun in [item.lower() for item in self.player.current_room.items.keys()]: # Allows you to take items
                self.player.take_item(self.player.current_room.remove_item(noun))

            elif verb == 'crafting' and noun == 'menu': # Allows you to craft weapons from what you pick up
                self.player.crafting()
                        
            elif verb == 'drop' and noun == 'weapon': # Allows you to drop items if you have to many
                self.player.drop_weapon()
    
            elif verb == 'equip' and noun in [item.name.lower() for item in self.player.inventory]: # Allows you to equip items yo attack with
                self.player.equip(self.player.get_object(noun))
   
            else:
                print("Invalid input")
        print("You were incapcitated, You're going away for a long time!")

    def intro(self):
        self.player.name = input("What is your name, Young adventurer? >>> ") # Asks for you name and inserts it into the story
        print("""
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    PROLOGUE: After a hardcore night of partying you wake with a massive hangover. You are on a park bench when you see a toad chilling on the sidewalk. 
You decide to lick it and out of nowhere a polive officer comes and handcuffs you and asks you to explain yourself. 
You are so hungover that you say "I'm sorry Mr. Budweiser I've not had as many officers as you think I have" The officer says "Sir are you drunk?" You reply with I swear to drunk I'm not god." 
Next thing you know your are in front of Judge Judith Sheindlin. The people are real, The cases are real, The ruling is final. 
    PLEASE RISE! """ + self.player.name + """, you have been sentenced to life in prison for licking a toad. 
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------""")
        user_input = input("Press enter to continue: ")
        if user_input == '':
            self.game_loop()
        else:
            print('Enter was not pressed')

    def outro(self):
        print("""
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
    Epilouge: After you defeat the all mighthy santa claus you see a man hole cover. This is the only option of escape. You lift the lid and slide down the pole down the manhole. You have no idea where you are at until
you see your pet goldfish going down the sewage. You know that you are close. You find 4 turtles eating pizza that give you directions to the nearest exit. When you exit you come up into a classroom. 
the classroom has a middle aged teacher and 21 students. All of them look like the type that would solve a rubix cube in the shower while slaying people on league of legneds, most of them would run at the sight of a female. 
You need to get back to your female, you run through the hall only to be stopped by THE ONE THE ONLY MRS FOSTER DUN NA NA NA,    DUN NA NA AN." She asks you why you are running in the halls and you tell that you're dog had kittens
and you need to get home immediately. She replied with "Your still in trouble your punishment is that you have to DAB for me." So you put your hands up and give her the biggest bestest longest spactatiolous DAB in the history of DABS
you then you speedwalk out to your Ford Mustang. Good thing you bought the fastest sports car ever and you race home get in the showew clean up and then you hear a DING DONG" You quickly put your pants on an and rush to the door and 
open the door and your date is the queen of england. Good luck """ + self.player.name + """. (Sorry Kiara we didn't have time to put in a gender thing and majority rules so looks like your just going to have to go on a date with a girl. Don't have too much fun)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------        
  
        THANKS FOR PLAYING 
            """)
        sys.exit(0)

    def help_info(self): # When command help is run you get this as a help
        print("""
    >>> To drop your equipped weapon do 'drop weapon'
    >>> To pick up an item type 'take' [item name]
    >>> To equip an item type 'equip' [item name]
    >>> To go to the next room type 'go' and the direction (north, south, east, west)
    >>> To RAGE quit the game type 'quit' or 'exit'
    >>> To go to the previous rooms type 'back'
    >>> To see what is craftable type 'crafting menu': Then type the weapons shown to craft it
    >>> To view your inventory type 'i' or 'inventory' 
        """)


# class that allows you to fight the enemys
class Combat():
    def active_combat(self, player, opponent, player_turn = True, previous_attack = None):
        print("A " + opponent.name + " appears")
        while player.health > 0 and opponent.health > 0:
            time.sleep(1.5)
            os.system('clear')
            print("_" * 28)
            print("Enemy health : " + "[+]" * int(opponent.health / 5))
            print("Your  health : " + "[+]" * int(player.health / 5))
            print("_" * 28)
            self.print_combat_panel(player)
            while player_turn:
                print("What will you do?")
                user_input = input('>>> ').lower()
                if user_input in [attack.lower() for attack in player.weapon.attacks.keys()]:
                    opponent.health -= player.attack(user_input)
                    player.weapon.decrease_durability(player.weapon.attacks[user_input])
                    previous_attack = player.weapon.attacks[user_input]
                    time.sleep(.5)
                    player_turn = False
                elif user_input == 'quit' or user_input == 'exit' or user_input == 'rage': # prints the Exit message
                    print("You Lose, Goodbye!")
                    sys.exit(0)
                elif user_input == 'i': # Allows you to access your Inventory in combat
                    print("::INVENTORY::")
                    for item in player.inventory:
                        print(item.name)
                    print("::INVENTORY::")

                elif user_input == 'swap weapon': # Allows you to randomly swap your equipped item with another
                    if len(player.inventory) > 0:
                        player.weapon = player.inventory[0]
                        os.system('clear')
                        self.print_combat_panel(player)
                    else:
                        print("No other weapons")
                else:
                    print("Invalid option (in active_combat)")

            player.health -= opponent.attack()
            time.sleep(.5)
            player_turn = True # Checks to see if you are able to attack
        if opponent.health <= 0: # Checks to see if the enemy is incapacitated
            print("%s has been incapacitated!" % (opponent.name))

    def print_combat_panel(self, player): # Shows you the enemys health and possible attacks
        print("_" * 28)
        print("-----------COMBAT-----------")
        print("_" * 28)
        print("ATTACK----------------DAMAGE")
        if player.weapon:    
            for key, val in player.weapon.attacks.items():
                print(key.capitalize() + " " * (26 - len(key + str(val))) + str(val) + " |")
        else:
            print("YOU HAVE NO WEAPON")
        print("_" * 28)


class Player(): # The players attributes such as health. Look down for more
    def __init__(self, name, health, inventory, weapon, current_room):
        self.name = name
        self.health = health
        self.inventory = inventory
        self.weapon = weapon
        self.current_room = current_room
        self.previous_rooms = []
    
    def print_room_menu(self): # Prints message where the player is currently at and if any possible enemies are in the room
        os.system('clear')
        self.check_for_enemy()
        print("_" * 28)
        self.current_room.print_area_message()
        self.current_room.print_exits()
        self.current_room.print_items()
        self.current_room.print_npcs() 
        print("_" * 28)

    def go_back(self): # User command to check to see if the player want to go back to the previous room.
        if self.previous_rooms == []:
            print ("There is no where to go back to.")
            print ("You are in " + self.current_room.name)
        else:
            self.current_room = self.previous_rooms.pop()
            self.print_room_menu()

    def change_rooms(self, new_room):
        self.new_room = new_room
        self.previous_rooms.append(self.current_room)
        self.current_room = self.new_room
        self.print_room_menu()
    
    def attack(self, attack): # User commands for attacking
        if attack in self.weapon.attacks.keys():
            print("You attacked doing %d" %(self.weapon.attacks[attack]))
            return self.weapon.attacks[attack]
        else:
            print("That is not a valid attack!")
            return 0

    def take_item(self, item_to_take): # User command for taking items
        if item_to_take:
            self.inventory.append(item_to_take)
            print("You took " + item_to_take.name)
        else:
            print("That item is not in this room")
            
    def drop_weapon(self): # User command for dropping items
        print("You dropped %s" %(self.weapon.name))
        self.weapon = None
    
    def equip(self, item_to_equip): # User command for equiping items
        if item_to_equip:
            self.inventory.append(self.weapon)
            self.weapon = item_to_equip
            self.inventory.remove(item_to_equip) 
            print("You equipped %s" %(item_to_equip.name))
        else:
            print("That thing is not equipable, or it was not spelled right")
    
    def crafting(self):
        craftable = {item.name.lower(): item for item in combo_weapons if set(item.requirements) & set(self.inventory) == set(item.requirements)}
        print("You can craft the following items:")
        for item in craftable.values():
            item.crafting_menu()
        while True:
            ("If you would like to craft any of them, type 'craft' and the item name")
            user_input_list = input('>>> ').lower().split()
            verb = ''
            noun = ''

            if len(user_input_list) >= 2:
                verb = user_input_list[0]
                noun = ' '.join(user_input_list[1:])

            if verb == 'craft' and noun in craftable.keys():
                for item in craftable[noun].requirements:
                    self.inventory.remove(item)
                self.inventory.append([item for item in combo_weapons if item.name.lower() == noun][0])
                print("You crafted a %s " % (noun))
                return
            else:
                print("Something about your input was incorrect, please try again.")

    def check_for_enemy(self): # Self explanitory
        del_enemies = []
        for npc in self.current_room.npcs.values():
            if type(npc) == Enemy:
                combat.active_combat(self, npc)
            if npc.health <= 0:
                del_enemies.append(npc)
        for npc in del_enemies:
            del_enemies.remove(npc)
    
    def get_object(self, checking_item):
        items_dict = {item.name.lower(): item for item in self.inventory}
        if checking_item.lower() in items_dict.keys():
            return items_dict[checking_item.lower()]
        else:
        	return None


class NPCS(): # Sets the Frame for NPCS
    def __init__(self, name, health, aggro, weapon):
        self.name = name
        self.health = health
        self.aggro = aggro
        self.weapon = weapon


class Enemy(): # Sets the Frame for Enemies, such as their health and weapon
    def __init__(self, name, health, weapon):
        self.name = name
        self.health = health
        self.weapon = weapon

    def attack(self):
        attack_list = [key for key in self.weapon.attacks]
        if self.health > 0 and self.weapon != None:
            queue_attack = self.weapon.attacks[random.choice(attack_list)]
            print(self.name + " attacked you doing " + str(queue_attack) + " damage!")
            return queue_attack
        else:
            return 0


# States the traits of a weapon and decreases the weapons durability
class Weapon():
    def __init__(self, name, durability, attacks):
        self.name = name
        self.durability = durability
        self.attacks = attacks
    
    def decrease_durability(self, value):
        if self.durability > 0 and self.durability - int(value / 3) > 0:
            self.durability -= int(value / 3)
            print("Weapon durability decreased to %d" %(self.durability))
        else:
            print("The weapon has broken! It does no damage!")
            self.durability = 0
            for key, val in self.attacks.items():
                self.attacks[key] = 0
                

# List the specifications of a combo Weapons
class ComboWeapon(Weapon):
    def __init__(self, name, durability, attacks, requirements):
        self.name = name
        self.durability = durability 
        self.attacks = attacks
        self.requirements = requirements
    
    def crafting_menu(self):
        print("_" * 28)
        print("REQ FOR " + self.name.upper())
        print("_" * 28)
        print("NAME--------------DURABILITY")
        print("_" * 28)
        for item in self.requirements:
            print(item.name + " " * (26 - len(item.name + str(item.durability))) + str(item.durability) + " |")
        print("_" * 28)


# Lists the attributes of an item
class Item():
    def __init__(self, name, special_val):
        self.name = name
        self.special_val = special_val


class Room(): # Sets the Fram for Rooms, responsible for handling all the stuff inside a room
    def __init__(self, name, location_message, exits, items, npcs):
        self.name = name
        self.location_message = location_message
        self.exits = exits
        self.items = {item.name.lower(): item for item in items}
        self.npcs = {npc.name: npc for npc in npcs}
    
    def print_area_message(self):
        print(self.location_message)

    def print_exits(self): # Test to see if there are any exits other than the one you came in from then prints them
        if len(self.exits) == 0:
            print("There are no apparent exits, besides the one you entered.")
        else:
            print("The exits of the room are: %s " % (", ".join(self.exits.keys())))

    def print_items(self):
        if len(self.items) == 0: # Tests to see if there are any items in the given room
            print("The room appears to be bare of anything useful to you.")
        else:
            print("The items in the room are: %s " % (", ".join([item.capitalize() for item in self.items.keys()])))

    def print_npcs(self): # Tests to see if there are any NPCS in the 
        if len(self.npcs) == 0:
            print("The room is empty of human presence")
        else:
            print("The people in the room are: %s " % (", ".join(self.npcs.keys())))

    def remove_item(self, item): # Takes the given item out of the current room
        if item in self.items.keys():
            return self.items.pop(item)
        else:
            return None


# Weapon instances
# name, durability {"attack": damage}


starter = Weapon("Starter weapon", 1, {'slice': 55})
longsword = Weapon("Excaliber", 75, {'side swipe' : 10, 'overhead swing' : 15})
RWS = Weapon("Rusty Wooden Spoon", 15, {"stab" : 3})
Butcher = Weapon("Butcher Knife", 40, {'slash' : 10, "overhead swing" : 14})
bowie = Weapon("Bowie Knife", 65, {"slash" : 16})
tooth_brush = Weapon("tooth brush shiv", 1, {"shank" : 33})
button = Weapon("Button", 100, {"stab" : 1})
soap = Weapon("Soap", 1, {"slather" : 1000})
butter= Weapon("Butter", 1, {"slather" : 4})
sock = Weapon("Sock", 20, {"choke" : 14})
garbage = Weapon("Garbage", 10, {"bash" : 3})
tv = Weapon("Televison", 18, {"bash" : 10})
xbox = Weapon("Xbox 360", 17, {"bash" : 13})
blade = Weapon("Blade of Grass", 2, {"slap" : 65})
basketball = Weapon("Basketball", 5, {"bash" : 14})
prison_stick = Weapon("Wacking Stick", 100, {"bash" : 15})
mail = Weapon("A piece of Mail", 20, {"slap" : 4})
santa_pack = Weapon("Santa's Present Bag", 100, {"bash": 80, "ground pound": 70, "dab": 0})# dab is ineffective
easter_egg = Weapon("Easter Egg", 350, {"easter": 99, "crack": 32})


# Combo Weapons
# name, durability, attack, requirements


butter_sock = ComboWeapon("Butter Sock", 50, {"overhead swing": 20, "power throw": 35}, [butter, sock])
warden_stick = ComboWeapon("Warden's Stick", 100, {"stab": 50, "ground pound": 80}, [prison_stick, blade, xbox])
soap_sock = ComboWeapon("Soap Sock", 40, {"overhead swing": 10, "power throw": 15}, [soap, sock])
combo_weapons = [butter_sock, warden_stick, soap_sock]
 
 
# NPCS instances            
# name, health, aggro, weapon


inmate_9215 = NPCS("Inmate 9215", 50, False, button)
dr_seuss = NPCS("Dr. Suess", 15, False, None)
inmate_4421 = NPCS("Inmate 4421", 63, False, tooth_brush)
inmate_2319 = NPCS("Inmate 2319", 23, False, sock)
oj = NPCS("O.J Simpson",23,False, None)
dog1 = NPCS("Barker", 150, False, None)
dog2 = NPCS("Bitter", 300, False, None)
guard1= NPCS("Sam Healy", 52, False, prison_stick)
cook1 = NPCS("Davros", 10, False, Butcher)
cook2 = NPCS('Jeff', 13, False, None)
hc = NPCS("Hillary Clinton",1,False, None)


#Enemy instances
# name, Health, weapon


ken = Enemy("Ken", 15, RWS)
rocco = Enemy("Rocco", 30, butter_sock) 
ace = Enemy("Ace", 50, bowie)
warden = Enemy("The Warden", 100, warden_stick)
garbage_monster = Enemy("The Garbage Monster", 35, garbage)
santa = Enemy("Saint Nicholas", 100, santa_pack)


# Area instances
# name message exits items npcs
# Name, Message, {exits}, [Weapon/item], [npc]:


window = Room('window', 'Out the Window', {}, [], [])
Jime = Room("jime", "Santa's Lair, you walk in on Mr and Mrs Claus, prepare for combat. This is the last battle before you can have freedom. You can already smell her perfume from here  ", {'east': window}, [],[santa])
wardens = Room("warden", "Warden's Office, She's pretty hot you can always ditch your hot date for the warden. Maybe the punishment is worth it ;) ", {"south": Jime}, [warden_stick], [warden])
office = Room("office", "Main Office, where the staff works at  wait is that HILLARY CLINTON??? ", {"east":wardens}, [], [hc])
kennel = Room("kennel", "Kennels for the K9's ", {}, [], [dog1, dog2])
fence = Room("fence", "Fence, can you smell the freedom yet?", {}, [blade], [ace]) #don't know yet
yard = Room("yard", "The Yard, the only part of the prison where there is life.", {"north":fence}, [basketball], [oj]) #turn oj into aggresive 
garbage = Room("garbage","Garbage Room, where the garbage monster lives", {"south": fence}, [garbage], [garbage_monster])
delivery = Room("delivery", "Delivery Room, this is the room where the food and supplies are for the prison", {"east": garbage}, [], [])
storage = Room("Storage", "Storage Room, the room of storage", {"south": delivery, "east": kennel}, [], [])
laundry = Room("Lanudry", "Lanudry Room, this is where laundry is done, Hint: These isn't anything useful in this room", {"south": storage}, [sock], [])
the_shu = Room("Shu", "The Shu aka Solitary confinment, there is no escaping this room", {}, [soap], [rocco]) # Leads nowhere and you die from there
mail_room = Room("Mail", "Mail Room this is where mail is sorter luckily your friend snuck in a weapon in the mail for you", {"south": delivery}, [mail], [])
commons = Room("Commons", "Common Room,This is the commons where you will be spending most of your time there are a lot of exits for you to take so choose wisely oh and BTW WE GOT A 23 19!!!!!!!!!!!!!!!!!!!!!!!!!!", {"north": yard, "south": mail_room, "east": office}, [tv, xbox], [inmate_2319])
corridor2 = Room("Corridor", "Another Corridor, this is a gateway rooms choose your next move carefully or else you might end up like Kelly the Killer Klown", {"north": the_shu, "south": laundry, "east": commons}, [button], [] )
kitchen = Room("Kitchen", "There seems to be a kitchen. This leads nowhere and this room provides no reserouces to you, Try not to be seen by the cooks though", {}, [Butcher], [cook1, cook2]) # Leads nowhere
mess_hall = Room("Mess Hall", "You have walked into a mess hall which leads to a kitchen nothing out of the ordinary here ", {"east": kitchen}, [RWS, butter], [inmate_4421])
med_bay = Room("Medical Bay", "There seems to be a medical bay you look to the right and you can see someone menically laughing and cutting up a body. The only way out to go back where you came from", {}, [], [dr_seuss]) # Leads nowhere
corridor = Room("Corridor", "You walk into a long spooky hall way where you see a creepy man at the end of the hall.", {"north": mess_hall, "south": med_bay, "east": corridor2}, [easter_egg], [inmate_9215, ken])
jail_cell = Room("Jail cell", "Next thing you know You wake up in a Jail cell with no recolation of anything, you look down and you have a strange tattoo inside your armpit, you have a hot date tonight and need to escape quickly ", {'east': corridor}, [tooth_brush, longsword], [])


# Starts the game and runs it on a loop


print(title_text)
combat = Combat()
game1 = Game(Player('', 85, [starter], starter, jail_cell))
game1.intro()