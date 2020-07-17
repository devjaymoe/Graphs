from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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
flag_path = []
direction_switcher = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

# helper function to find the direction that hasn't been traveled
def find_untraveled_path(direction_dict):
    for k, v, in direction_dict.items():
        if v == "?":
            return k
    # return true if no path is untraveled
    return False

def graph_completed_check(traversal_graph):
    for k in traversal_graph:
        if traversal_graph[k]['completed'] == False:
            return False
    return True

def room_completed_check(room):
    for key, value in traversal_graph[room].items():
        if value == '?':
            traversal_graph[room]['completed'] = False
            return False
        else:
            traversal_graph[room]['completed'] = True
    return True

stack = []
room_exits = player.current_room.get_exits()
random_room_direction = random.choice(room_exits)
stack.append(random_room_direction)

# build out inital room
traversal_graph[player.current_room.id] = {}
for room_exit in room_exits:
    traversal_graph[player.current_room.id][room_exit] = '?'
traversal_graph[player.current_room.id]['completed'] = False

while graph_completed_check(traversal_graph) == False:
    # print('Current Room: ', player.current_room.id, 'Current Direction: ', stack[-1])
    # print(player.current_room.id)
    # the current direction being traveled
    current_direction = stack[-1]
    # reference to the previous room
    previous_room = player.current_room.id
    # traveling in the direction
    player.travel(current_direction)
    # add to flag path to turn around when needed
    # flag_path.append(current_direction)
    # print('Stack: ', stack)
    # print('flag path: ', flag_path)
    # add to travel path to keep track of all steps
    traversal_path.append(current_direction)
    # current room id
    current_room = player.current_room.id
    # print(current_room)
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
        
        traversal_graph[current_room]['completed'] = False

    # direction switcher
    previous_direction = direction_switcher[current_direction]
    traversal_graph[current_room][previous_direction] = previous_room

    # check if room has been completely searched
    cur_room_complete = room_completed_check(current_room)
    prev_room_complete = room_completed_check(previous_room)

    if graph_completed_check(traversal_graph) is True:
        break
    
    # in the current room, find a direction that has not been traveled
    untraveled_path = find_untraveled_path(traversal_graph[current_room])

    if untraveled_path is False:
        # this section will also be hit when retracing our steps
        # last_direction_travled = stack.pop()
        # direction_flipped = direction_switcher[last_direction_travled]
        # player.travel(direction_flipped)
        # print('before while loop', current_room)
        while untraveled_path is False:
            last_direction_travled = stack.pop()
            direction_flipped = direction_switcher[last_direction_travled]
            player.travel(direction_flipped)
            current_room = player.current_room.id
            traversal_path.append(direction_flipped)
            # print('Current Room in UP: ', current_room)
            untraveled_path = find_untraveled_path(traversal_graph[current_room])
        stack.append(untraveled_path)

        # if len(stack) == 0:
        #     # reverses path once hitting a dead end and attaches entire path to stack
        #     # for i in range(len(flag_path)):
        #     #     flag_path[i] = direction_switcher[flag_path[i]]
        #     # for x in flag_path:
        #     #     stack.insert(0, x)
        #     # flag_path = []
        # # if the stack is greater than 1 then we are in the process of retracing our steps
        # # but we have made a diversion and we've reached a dead end
        # elif len(stack) > 0 and len(flag_path) > len(stack):
        #     # if 
        #     for i in range(len(stack)):
        #         flag_path.pop(i)
        #     for i in range(len(flag_path)):
        #         flag_path[i] = direction_switcher[flag_path[i]]
        #     for x in flag_path:
        #         stack.insert(0, x)
        #     flag_path = []
    else:
        # I've hit a room with an untraveled path
        # if the previous room is completed then we dont need to go that way again
        # and can reset our flag path
        # if prev_room_complete is True and len(stack) == 0:
        #     # flag_path = []
        #     stack.append(untraveled_path)
        # else:
        stack.append(untraveled_path)

# print(graph_completed_check(traversal_graph))
# print(flag_path)
# print('Traversal Graph:', traversal_graph)

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
