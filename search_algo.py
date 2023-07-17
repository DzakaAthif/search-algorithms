import heapq
from math import ceil
import time

def task6(algorithm, message_filename, dictionary_filename, threshold, letters, debug):

    lines = ""
    with open(message_filename, "r") as file:
        lines = file.readlines()

    message = ""
    for item in lines:
        message += item

    # load dictionary into set so the running time is O(1)
    dictionary = set(line.strip() for line in open(dictionary_filename))
    # with open(dictionary_filename, "r") as file:
    #     for line in file:
    #         dictionary.append(line.strip())

    letters = list(letters)
    letters.sort()

    result = ""

    if algorithm == "d":
        result = dfs_bfs(message_filename, algorithm, 
                    message, dictionary, letters, 
                    threshold, debug, True)
    elif algorithm == "b":
        result = dfs_bfs(message_filename, algorithm, 
                    message, dictionary, letters, 
                    threshold, debug, False)
    elif algorithm == "i":
        result = ids(message_filename, algorithm, 
                    message, dictionary, letters, 
                    threshold, debug)
    elif algorithm == "u":
        result = ucs(message_filename, algorithm, 
                    message, dictionary, letters, 
                    threshold, debug)
    elif algorithm == "g":
        result = greedy(message_filename, algorithm, 
                    message, dictionary, letters, 
                    threshold, debug)
    elif algorithm == "a":
        result = a_star(message_filename, algorithm, 
                    message, dictionary, letters, 
                    threshold, debug)

    else:
        return "algorithm is not recognised"

    return result


# Algorithm--------------------------------------------------------------------

def greedy(filename, algo, message, dictionary, 
        letters, threshold, debug):
    
    solution = ""
    key = ""
    cost = 0
    max_depth = 0
    max_fringe = 0

    first_expanded = []
    expanded_count = 0
    global_idx = 0

    q = [(0, 0, global_idx, message, "")]
    heapq.heapify(q)

    while True:
        # get the last item in the list
        depth = 0
        target = ""
        path = ""

        # to avoid the IndexError if the heapq is empty
        size = len(q)
        if size == 1:
            h, idx, depth, target, path = q[0]
        else:
            h, idx, depth, target, path = heapq.heappop(q)

        # stop searching once 1000 nodes are expanded
        if expanded_count == 1000:
            break

        # print("type of target: {}".format(type(target)))

        # check if the item fulfilled the threshold
        passed = is_passed(target, dictionary, threshold)

        expanded_count+=1

        if len(first_expanded) < 10:
            first_expanded.append(target)

        if depth > max_depth:
            max_depth = depth
        
        if passed == True:
            # print("final result h value is: {}".format(h))
            solution = target
            key = path
            cost = depth
            break
        
        # expand if the item doesnt fulfill the threshold
        expanded, global_idx = expands_h(target, letters, path, 
                                depth, global_idx)
        
        # no need to add the expanded if its empty
        if len(expanded) == 0:
            continue
        
        # add the expanded nodes
        for item in expanded:
            heapq.heappush(q, item)

        # to remove the root node (it's already expanded)
        if (expanded_count == 1):
            heapq.heappop(q)

        if len(q) > max_fringe:
            max_fringe = len(q)
    
    ret = gen_ret_mssg(filename, algo, solution, key, cost, 
            expanded_count, max_fringe, max_depth, 
            first_expanded, debug)

    return ret

def a_star(filename, algo, message, dictionary, 
        letters, threshold, debug):
    solution = ""
    key = ""
    cost = 0
    max_depth = 0
    max_fringe = 0

    first_expanded = []
    expanded_count = 0
    global_idx = 0

    q = [(0, global_idx, 0, message, "")]
    heapq.heapify(q)

    cache_is_passed = set()
    cache_h_dict = {}

    while True:
        # get the last item in the list
        depth = 0
        target = ""
        path = ""

        # to avoid the IndexError if the heapq is empty
        if len(q) == 1:
            f, idx, depth, target, path = q[0]
        else:
            # should expand last? added node if with same priority
            f, idx, depth, target, path = heapq.heappop(q)

        # stop searching once 1000 nodes are expanded
        if expanded_count == 1000:
            break

        expanded_count+=1

        if len(first_expanded) < 10:
            first_expanded.append(target)

        if depth > max_depth:
            max_depth = depth
        
        expanded = []
        if target not in cache_is_passed:

            # check if the item fulfilled the threshold
            passed = is_passed(target, dictionary, threshold)
            # print("expanded_count: {}".format(expanded_count))
            
            if passed == True:
                solution = target
                key = path
                cost = depth
                break

            cache_is_passed.add(target)
            
        # expand if the item doesnt fulfill the threshold
        expanded, global_idx = expands_f(target, letters, path, 
                                depth, global_idx, cache_h_dict)
        
        # no need to add the expanded if its empty
        if len(expanded) == 0:
            continue
        
        # add the expanded nodes
        for item in expanded:
            heapq.heappush(q, item)

        # to remove the root node (it's already expanded)
        if (expanded_count == 1):
            heapq.heappop(q)

        if len(q) > max_fringe:
            max_fringe = len(q)
    
    ret = gen_ret_mssg(filename, algo, solution, key, cost, 
            expanded_count, max_fringe, max_depth, 
            first_expanded, debug)

    return ret

def dfs_bfs(filename, algo, message, dictionary, 
        letters, threshold, debug, is_dfs):
    
    solution = ""
    key = ""
    cost = 0
    max_depth = 0
    max_fringe = 0

    first_expanded = []
    expanded_count = 0

    q = [(0, message, "")]
    while len(q) != 0:
        # get the last item in the list
        target = ""
        path = ""
        depth = 0

        if is_dfs == True:
            depth, target, path = q.pop()
        else:
            depth, target, path = q.pop(0)

        # stop searching once 1000 nodes are expanded
        if expanded_count == 1000:
            break

        # check if the item fulfilled the threshold
        passed = is_passed(target, dictionary, threshold)

        expanded_count+=1

        if len(first_expanded) < 10:
            first_expanded.append(target)

        if depth > max_depth:
            max_depth = depth
        
        if passed == True:
            solution = target
            key = path
            cost = depth
            break
        
        # expand if the item doesnt fulfill the threshold
        expanded, idx = expands(target, letters, path, depth, None)
        
        # no need to add the expanded if its empty
        if len(expanded) == 0:
            continue

        # add the expanded nodes
        if is_dfs == True:
            j = -1
            for i in range(len(expanded)):
                q.append(expanded[j])
                j-=1
        else:
            q.extend(expanded)

        if len(q) > max_fringe:
            max_fringe = len(q)
    
    ret = gen_ret_mssg(filename, algo, solution, key, cost, 
            expanded_count, max_fringe, max_depth, 
            first_expanded, debug)

    return ret

def ids(filename, algo, message, dictionary, 
        letters, threshold, debug):
    
    solution = ""
    key = ""
    cost = 0
    max_depth = 0
    max_fringe = 1

    first_expanded = []
    expanded_count = 0

    boundary = 0
    finished = False
    while True:

        q = [(0, message, "")]

        while len(q) != 0:
            # get the last item in the list
            depth, target, path = q.pop()

            # stop searching once 1000 nodes are expanded
            if expanded_count == 1000:
                finished = True
                break

            # check if the item fulfilled the threshold
            passed = is_passed(target, dictionary, threshold)

            expanded_count+=1

            if len(first_expanded) < 10:
                first_expanded.append(target)

            if depth > max_depth:
                max_depth = depth
            
            if passed == True:
                solution = target
                key = path
                cost = depth
                finished = True
                break

            if depth == boundary:
                continue
            
            # expand if the item doesnt fulfill the threshold
            expanded, idx = expands(target, letters, path, 
                        depth, None)

            # no need to add the expanded if its empty
            if len(expanded) == 0:
                continue

            # add the expanded nodes
            j = -1
            for i in range(len(expanded)):
                q.append(expanded[j])
                j-=1

            if len(q) > max_fringe:
                max_fringe = len(q)
        
        if finished == True:
            break

        boundary+=1
    
    ret = gen_ret_mssg(filename, algo, solution, key, cost, 
            expanded_count, max_fringe, max_depth, 
            first_expanded, debug)

    return ret

def ucs(filename, algo, message, dictionary, 
        letters, threshold, debug):
    
    solution = ""
    key = ""
    cost = 0
    max_depth = 0
    max_fringe = 0

    first_expanded = []
    expanded_count = 0
    global_idx = 0

    q = [(0, global_idx, message, "")]
    heapq.heapify(q)

    while True:
        # get the last item in the list
        depth = 0
        target = ""
        path = ""

        # to avoid the IndexError if the heapq is empty
        size = len(q)
        if size == 1:
            depth, idx, target, path = q[0]
        else:
            depth, idx, target, path = heapq.heappop(q)

        # stop searching once 1000 nodes are expanded
        if expanded_count == 1000:
            break

        # check if the item fulfilled the threshold
        passed = is_passed(target, dictionary, threshold)

        expanded_count+=1

        if len(first_expanded) < 10:
            first_expanded.append(target)

        if depth > max_depth:
            max_depth = depth
        
        if passed == True:
            solution = target
            key = path
            cost = depth
            break
        
        # expand if the item doesnt fulfill the threshold
        expanded, global_idx = expands(target, letters, path, 
                                depth, global_idx)
        
        # no need to add the expanded if its empty
        if len(expanded) == 0:
            continue
        
        # add the expanded nodes
        for item in expanded:
            heapq.heappush(q, item)

        # to remove the root node (it's already expanded)
        if (expanded_count == 1):
            heapq.heappop(q)

        if len(q) > max_fringe:
            max_fringe = len(q)
    
    ret = gen_ret_mssg(filename, algo, solution, key, cost, 
            expanded_count, max_fringe, max_depth, 
            first_expanded, debug)

    return ret


# Other functions--------------------------------------------------------------

def heuristic(message):

    message = message
    wrong_count = 0

    # if threshold == False:
    specific_letters = ["E", "T", "A", "O", "N", "S"]
    freq = {'A':0, 'E':0, 'N':0, 'O':0, 'S':0, 'T':0}

    for char in message:
        for letter in specific_letters:
            if letter == char or letter.lower() == char:
                count = freq.get(letter)
                freq[letter] = count + 1

    freq = list(freq.items())

    new_ls = []
    freq.sort()
    for i in range(len(freq)):
        letter, count = freq[i]
        new_ls.append((letter, count, i))

    new_ls.sort(key=sort_key, reverse=True)

    for i in range(len(specific_letters)):
        if specific_letters[i] != new_ls[i][0]:
            wrong_count+=1

    wrong_count = ceil(wrong_count/2)

    return wrong_count
    
def sort_key(item):
    return item[1], -item[2] 


def gen_ret_mssg(filename, algo, solution, 
        key, cost,expanded_count, max_fringe,  
        max_depth, first_expanded, debug):
    
    ret = "-----TERMINATED-----\n"
    ret += f"File Name: {filename}\nAlgorithm Used: "

    if algo == "d":
        ret+="Depth First Search\n\n"
    elif algo == "b":
        ret+="Breath First Search\n\n"
    elif algo == "i":
        ret+="Iterative Deepening Search\n\n"
    elif algo == "u":
        ret+="Uniform Cost Search\n\n"
    elif algo == "g":
        ret+="Greedy Search\n\n"
    elif algo == "a":
        ret+="A* Search\n\n"
    
    if len(solution) != 0:
        # there is a solution
        ret += "Solution: {}\n\n".format(solution)
        ret += "Key: {}\n".format(key)
        ret += "Path Cost: {}\n\n".format(cost)
    else:
        # there is no solution
        ret += "No solution found.\n\n"

    ret += "Num nodes expanded: {}\n".format(expanded_count)
    ret += "Max fringe size: {}\n".format(max_fringe)
    ret += "Max depth: {}".format(max_depth)

    if debug == 'y':
        ret += "\n\nFirst few expanded states:\n"
        for item in first_expanded:
            ret = ret + item + "\n\n"

        ret = ret.rstrip()
    
    return ret
    

def is_passed(message, dictionary, threshold):

    message = message.replace("\n", " ")
    message = message.strip()
    message = message.split(" ")
    
    correct = 0

    for word in message:
        word = word.lower()
        word = word.strip()
        word = word.translate({ord(i): None for i in ",.?!:;\"'()"})
    
        # check if word is in dictionary set
        if word in dictionary:
            correct += 1
    
    percent = ((correct)/len(message))*100

    if percent >= threshold:
        return True
    else:
        return False

# ------------------------------------------------------------------------------------------
# For heuristic algorithms
def expands_h(target, letters, path, depth, idx):
    expanded = []

    for i in range(len(letters)):
        for k in range(i+1, len(letters)):
            switched = switch_letters(target, (letters[i], letters[k]))
            
            if len(switched) != 0:
                path_cpy = path + letters[i] + letters[k]
                depth_cpy = depth + 1

                h = heuristic(switched)
                # print("{} node's h value is: {}".format(path_cpy, h))

                expanded.append((h, idx, depth_cpy, switched, path_cpy))
                idx+=1


    return (expanded, idx)

def expands_f(target, letters, path, depth, idx, cache_h_dict):
    expanded = []

    for i in range(len(letters)):
        for k in range(i+1, len(letters)):
            switched = switch_letters(target, (letters[i], letters[k]))
            
            if len(switched) != 0:
                path_cpy = path + letters[i] + letters[k]
                depth_cpy = depth + 1
                
                h = 0

                # if switched in cache
                if switched in cache_h_dict:
                    h = cache_h_dict.get(switched)
                else:
                    h = heuristic(switched)
                    cache_h_dict[switched] = h

                f = h + depth_cpy
                # print("{} node's f value is: {} + {} = {}".format(path_cpy, h, depth_cpy, f))

                expanded.append((f, idx, depth_cpy, switched, path_cpy))
                idx+=1

    return (expanded, idx)

def expands_f_cache(temp, depth, path, global_idx, cache_h_dict):

    expanded = []

    for child in temp:
        f, idx, d, mssg, p = child
        depth_cpy = depth + 1

        h = cache_h_dict.get(mssg)
        f = h + depth_cpy
        
        print(p[-2:], global_idx)
        path_cpy = path + p[-2:]

        expanded.append((f, global_idx, depth_cpy, mssg, path_cpy))
        global_idx+=1

    return (expanded, global_idx)

def expands(target, letters, path, depth, idx):
    expanded = []

    for i in range(len(letters)):
        for k in range(i+1, len(letters)):
            switched = switch_letters(target, (letters[i], letters[k]))
            
            if len(switched) != 0:
                path_cpy = path + letters[i] + letters[k]
                depth_cpy = depth + 1

                if (idx != None):
                    expanded.append((depth_cpy, idx, switched, path_cpy))
                    idx+=1
                else:
                    expanded.append((depth_cpy, switched, path_cpy))

    return (expanded, idx)

def switch_letters(message, letters):
    
    message = list(message)

    lower_lett = letters[0]+letters[1]
    lower_lett = lower_lett.lower()

    condition = (letters[0] not in message) \
        and (letters[1] not in message) \
        and (lower_lett[0] not in message) \
        and (lower_lett[1] not in message)
    
    if condition == True:
        return ""

    for i in range(len(message)):
        if message[i] == letters[0]:
            message[i] = letters[1]
        
        elif message[i] == letters[1]:
            message[i] = letters[0]
        
        elif message[i] ==  lower_lett[0]:
            message[i] = lower_lett[1]
        
        elif message[i] ==  lower_lett[1]:
            message[i] = lower_lett[0]

    return "".join(message)


if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task6 function
    print(task6('g', 'secret_msg.txt', 'common_words.txt', 90, 'AENOST', 'n'), end="\n\n")
    print(task6('a', 'scrambled_quokka3.txt', 'common_words.txt', 90, 'AENOST', 'n'), end="\n\n")
    print(task6('d', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'n'), end="\n\n")
    print(task6('b', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'n'), end="\n\n")
    print(task6('i', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'n'), end="\n\n")
    print(task6('u', 'spain.txt', 'common_words.txt', 80, 'AE', 'n'))
