import yaml
import pdb
input_file = open("palace.csv", "r")
output_file = open("palace.yaml", "w")


rooms = input_file.readlines()
room_exits_dict = {}

# [[this room, other room, other room], [room here, here, and here]]

for index, row in enumerate(rooms):
	row = row.rstrip().split(",")
	row_index  = index
	print(row)
	for index, room in enumerate(row):
		room_exits = []
		if row_index != 0:
			up_room = rooms[row_index - 1][index]
			room_exits.append(up_room)
		if row_index != len(rooms) - 1:
			down_room = rooms[row_index + 1][index]
			room_exits.append(down_room)
		if index != 0:
			left_room = row[index - 1]
			room_exits.append(left_room)
		if index != len(row) - 1:
			print(str(index))
			right_room = row[index + 1]
			room_exits.append(right_room)
		room_exits_dict[room] = room_exits

print(room_exits_dict)

output_file.write(yaml.dump(room_exits_dict, default_flow_style = False)) 	

input_file.close()
output_file.close()






