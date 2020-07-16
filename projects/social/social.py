import random
import time

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.reset()

    def reset(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            # print("WARNING: You cannot be friends with yourself")
            return False
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            # print("WARNING: Friendship already exists")
            return False
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
        
        return True # Success!

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.reset()
        # !!!! IMPLEMENT ME

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i}")

        # Create friendships
        possible_friendships = []

        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        # Shuffle the possbile friendships
        random.shuffle(possible_friendships)

        # add friendships
        for i in range(num_users * avg_friendships // 2):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])

    def populate_graph_2(self, num_users, avg_friendships):
        # reset graph
        self.reset()

        # add users
        for i in range(num_users):
            self.add_user(f'User {i+1}')

        # create friendships
        target_friendships = num_users * avg_friendships
        total_friendships = 0
        collisions = 0

        while total_friendships < target_friendships:
            user_id = random.randint(1, self.last_id)
            friend_id = random.randint(1, self.last_id)

            if self.add_friendship(user_id, friend_id):
                total_friendships += 2
            else:
                collisions += 1

        print(f'collisions: {collisions}')

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        # !!!! IMPLEMENT ME
        if user_id not in self.friendships:
            return visited

        queue = []
        path = [user_id]
        queue.insert(0, path)
        visited = {}  # Note that this is a dictionary, not a set

        while len(queue) > 0:
           path = queue.pop(0)

           last_friend = path[-1]

           if last_friend not in visited:

               visited[last_friend] = path

               for next_friend in self.friendships[last_friend]:

                   next_path = path + [next_friend]

                   queue.append(next_path)

        return visited

if __name__ == '__main__':
    sg = SocialGraph()

    num_users = 1000
    avg_friendships = 5

    if num_users / avg_friendships > 2:
        sg.populate_graph(num_users, avg_friendships)
    else:
        sg.populate_graph_2(num_users, avg_friendships)

    # start_time = time.time()
    # sg.populate_graph(num_users, avg_friendships)
    # end_time = time.time()
    # print(f'O(n^2) runtime: {end_time - start_time}')

    # start_time = time.time()
    # sg.populate_graph_2(num_users, avg_friendships)
    # end_time = time.time()
    # print(f'O(n) runtime: {end_time - start_time}')

    # print('Friendships: ', sg.friendships)
    # connections = sg.get_all_social_paths(1)
    # print(connections)

    # accum = 0
    # for friend in sg.friendships:
    #     connects = sg.get_all_social_paths(friend)
    #     # print(f'{friend}\'s connections: {connects}')
    #     accum += len(connects)

    # accum //= len(sg.friendships)
    # print('Average length of connections: ', accum)
    # print('precent of conections?: ', accum / len(sg.friendships))
    