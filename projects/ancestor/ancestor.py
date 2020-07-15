def earliest_ancestor(ancestors, starting_node):
    # check if node is in ancestors data and pull it out of it
    found_node = None

    for node in ancestors:
        # found node as a child in a node pair
        if starting_node is node[1]:
            found_node = node
            break
    
    if found_node is None:
        return -1

    visited = set()
    queue = []
    queue.insert(0, found_node)

    while len(queue) > 0:
        node = queue.pop(0)
        # check if node is parent to starting node
        parent = node[0]
        if node not in visited:
            visited.add(node)
            # find a parent pointing to this node
            for ancestor in ancestors:
                # a parent node pointing to another parent
                if ancestor[1] is parent:
                    # queue that to check again
                    queue.append(ancestor)
                    break
    return parent

if __name__ == '__main__':
    test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]

    print(earliest_ancestor(test_ancestors, 11))