# -------------------------------------- test 1
def solution1(x, y):
    # write your code in Python
    results = ""
    for c in x:
        if c in y:
            results += c

    if y in results:
        return True
    return False


def add_connection(results, name1, name2):
    if name1 in results:
        results[name1].add(name2)
    else:
        results[name1] = {name2}


def convert_connections_to_dict(connections):
    results = {}
    for v in connections:
        name1, name2 = v.split(":")
        add_connection(results, name1, name2)
        add_connection(results, name2, name1)
    return results


# ------------------------------------------- test 2
def get_connections_between_names(name1, name2, dict_connections):
    if name1 == name2:
        return [name1]

    list_of_connection = [[name1]]
    i = 0
    pre_conn = {name1}

    while len(list_of_connection) > i:
        now_path = list_of_connection[i]
        last_name = now_path[-1]
        next_names = dict_connections[last_name]

        if name2 in next_names:
            now_path.append(name2)
            return now_path

        for next_name in next_names:
            if next_name not in pre_conn:
                new_name = now_path[:]
                new_name.append(next_name)
                list_of_connection.append(new_name)
                pre_conn.add(next_name)
        i += 1
    return []


def solution2(connections, name1, name2):
    graph = convert_connections_to_dict(connections)
    results = get_connections_between_names(name1, name2, graph)
    return len(results) - 1
