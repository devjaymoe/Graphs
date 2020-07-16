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

stack = []
room_exits = player.current_room.get_exits()
random_room_direction = random.choice(room_exits)
stack.append(random_room_direction)

# build out inital room
traversal_graph[player.current_room.id] = {}
for room_exit in room_exits:
    traversal_graph[player.current_room.id][room_exit] = '?'

# THIS TAKES ME DOWN A PATH UNTIL I REACH A POINT WHERE THERE ARE NO UNKOWN ROOMS
while len(stack) > 0:
    # the current direction being traveled
    current_direction = stack.pop()
    # reference to the previous room
    previous_room = player.current_room.id
    # traveling in the direction
    player.travel(current_direction)
    # current room id
    current_room = player.current_room.id
    print(current_room)
    # all of the exits from this room in an array
    room_exits = player.current_room.get_exits()

    # fill out the known values in the traversal graph
    traversal_graph[previous_room][current_direction] = current_room

    # place current room in traversal graph
    if current_room not in traversal_graph:
        traversal_graph[current_room] = {}

        # place room in graph and give it all the exits
        for room_exit in room_exits:
            traversal_graph[current_room][room_exit] = '?'
    
    # getting the opposite direction from the one we came from
    reverse_direction = direction_switcher[current_direction]
    # placing that value in the graph of known directions
    traversal_graph[current_room][reverse_direction] = previous_room

    # in the current room, find a direction that has not been traveled
    for direction in traversal_graph[current_room]:
        if traversal_graph[current_room][direction] == '?':
            # go in that direction
            stack.append(direction)

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
