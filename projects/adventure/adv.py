from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
traversal_graph = {}
direction_switcher = { 'n': 's', 's': 'n', 'e': 'w', 'w': 'e' }

def make_graph_entry(room):
    traversal_graph[room] = []
    traversal_graph[room].append(False)
    traversal_graph[room].append({})

def find_unkown_direction(direction_dict):
    for key, val in direction_dict.items():
        if val == '?':
            return key
    return True

# build out inital room
room_exits = player.current_room.get_exits()
make_graph_entry(player.current_room.id)

for room_exit in room_exits:
    traversal_graph[player.current_room.id][1][room_exit] = '?'

stack = []
stack.append(player.current_room.id)
# THIS TAKES ME DOWN A PATH UNTIL I REACH A POINT WHERE THERE ARE NO UNKOWN ROOMS
while len(stack) > 0:
    # the current room being traveled
    current_room = stack.pop()
    # reference to the previous room
    previous_room = current_room
    # all of the exits from this room in an array
    room_exits = player.current_room.get_exits()
    # pick a random direction to go in
    random_room_direction = random.choice(room_exits)
    # traveling in the direction
    player.travel(random_room_direction)
    # new current room id
    current_room = player.current_room.id
    # new exits
    room_exits = player.current_room.get_exits()

    # place current room in traversal graph
    if current_room not in traversal_graph:
        make_graph_entry(current_room)

        # place room in graph and give it all the exits
        for room_exit in room_exits:
            traversal_graph[current_room][1][room_exit] = '?'

    # fill out the known values in the traversal graph
    traversal_graph[previous_room][1][random_room_direction] = current_room
    # getting the opposite direction from the one we came from
    reverse_direction = direction_switcher[random_room_direction]
    # placing that value in the graph of known directions
    traversal_graph[current_room][1][reverse_direction] = previous_room

    print(find_unkown_direction(traversal_graph[current_room][1]))


print('Traversal Graph:', traversal_graph)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
