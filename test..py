def handle_user_input(self):
        # Could remerge this function and handle_language
        while True:
            print("\n")
            user_input_list = input(">>>").split()
            
            user_input = ''
            if len (user_input_list) == 1:
                user_input = user_input_list[0]
            
                        possible_adjectives = ["with"] # Temporary fix for entering handle_language twice with the 2 if statements below, working and the printing the fail state. 
            if len(user_input_list) >= 2: 
                self.handle_language(self.player1, self.current_room, " ".join(user_input_list[1:]), user_input_list[0].lower())

            if len(user_input_list) == 3 and user_input_list[1] in possible_adjectives: #Temporary fix for interacting with NPCs, change to account for this in the previous statment later
                self.handle_language(self.player1, self.current_room, " ".join(user_input_list[2:]), user_input_list[0].lower(), user_input_list[1])
            
            elif user_input == 'i':
                print("______________________\nINVENTORY\n______________________")    
                for item in self.player1.inventory:
                    spaces = " " * (20 - len(item.name))
                    print(item.name + spaces)
                print("______________________")
                
            elif user_input == 'g':
                print(self.player1.gold)

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
            self.current_room = self.current_room.exits[self.noun]
            self.print_room_messages()

        elif self.verb == 'equip' and self.noun in self.all_items_dictionary().keys():
             self.player.change_equipment(self.noun)

        elif self.verb == 'attack' and self.noun in self.current_room.npcs.keys():
            npc_to_attack = self.current_room.npcs[self.noun]
            self.player.attack(npc_to_attack)
        
        elif self.verb == 'use' and self.noun in item_names.keys():
            self.all_items_dictionary()[self.noun].special_property_use(current_room)

        elif self.verb == 'check' and self.noun in item_names:
            print(item_names[self.noun].description)

        elif self.verb == 'check' and self.noun == 'equipment':
            print("Weapon: " + self.player.weapon.name)
            print("Head: " + self.player.armor["head"].name)
            print("Chest: " + self.player.armor["chest"].name)
            print("Legs: " + self.player.armor["legs"].name)

        else:
            print("Invalid option!(In handle_language)")
            
            
            
"""def handle_user_input(self):
        # Could remerge this function and handle_language
        while True:
            print("\n")
            user_input_list = input(">>>").split()
            user_input = ''
            if len (user_input_list) == 1:
                user_input = user_input_list[0]
            
            possible_adjectives = ["with"] # Temporary fix for entering handle_language twice with the 2 if statements below, working and the printing the fail state. 
            if len(user_input_list) >= 2: 
                self.handle_language(self.player1, self.current_room, " ".join(user_input_list[1:]), user_input_list[0].lower())

            if len(user_input_list) == 3 and user_input_list[1] in possible_adjectives: #Temporary fix for interacting with NPCs, change to account for this in the previous statment later
                self.handle_language(self.player1, self.current_room, " ".join(user_input_list[2:]), user_input_list[0].lower(), user_input_list[1])

            elif user_input == 'i':
                print("______________________\nINVENTORY\n______________________")    
                for item in self.player1.inventory:
                    spaces = " " * (20 - len(item.name))
                    print(item.name + spaces)
                print("______________________")
                
            elif user_input == 'g':
                print(self.player1.gold)

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
            self.current_room = self.current_room.exits[self.noun]
            self.print_room_messages()

        elif self.verb == 'equip' and self.noun in self.all_items_dictionary().keys():
             self.player.change_equipment(self.noun)

        elif self.verb == 'attack' and self.noun in self.current_room.npcs.keys():
            npc_to_attack = self.current_room.npcs[self.noun]
            self.player.attack(npc_to_attack)
        
        elif self.verb == 'use' and self.noun in item_names.keys():
            self.all_items_dictionary()[self.noun].special_property_use(current_room)

        elif self.verb == 'check' and self.noun in item_names:
            print(item_names[self.noun].description)

        elif self.verb == 'check' and self.noun == 'equipment':
            print("Weapon: " + self.player.weapon.name)
            print("Head: " + self.player.armor["head"].name)
            print("Chest: " + self.player.armor["chest"].name)
            print("Legs: " + self.player.armor["legs"].name)

        else:
            print("Invalid option!(In handle_language)")"""