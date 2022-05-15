import heapq
import copy

# goal = [
#     [1,2,3],
#     [4,5,6],
#     [7,8,0]]

def generate_goal(n):
    """
    generate the goal of the n*n puzzle
    :param n: puzzle width
    :return: the goal state
    """
    goal = []
    for i in range(n):
        goal.append([])
        for j in range(n):
            goal[i].append(i*n + j + 1)
    goal[-1][-1] = 0
    return goal

def misplaced_heuristics(state):
    """
    calculate the number of the misplaced tiles
    :param state:
    :return:
    """
    n = len(state)
    h = 0
    for i in range(n):
        for j in range(n):
            if state[i][j] != i*n + j + 1 and state[i][j] > 0:
                h += 1
    return h


def manhattan_heuristics(state):
    """
    calculate the number of move
    :param state:
    :return:
    """
    n = len(state)
    h = 0
    for i in range(n):
        for j in range(n):
            currNum = state[i][j]
            if currNum == 0:
                continue
            rightPlaceX = (currNum-1)//n
            rightPlaceY = (currNum-1)%n
            h += abs(rightPlaceX - i) + abs(rightPlaceY - j)
    return h


def blank_move_direction(state,direction):
    """
    move the blank and return the new state
    :param state: origin state
    :param direction: the direction you want to moved (up, down, left, right)
    :return: the new state after move.
    """
    n = len(state)
    for i in range(n):
        for j in range(n):
            if state[i][j] == 0:
                x0 = i
                y0 = j
                break
        if state[i][j] == 0:
                break

    move = {'up':[-1,0],'down':[+1,0],'left':[0,-1],'right':[0,+1]}
    x1 = x0 + move[direction][0]
    y1 = y0 + move[direction][1]
    if x1 < 0 or n <= x1 or y1 < 0 or n <= y1 :
        return None
    state[x0][y0] = state[x1][y1]
    state[x1][y1] = 0
    return state


def uniform_cost_serch(state):
    """
    :param state: state
    :return: 0
    """
    return 0

def default_case(case_id):
    """
    select default case
    :param case_id:
    :return:
    """

    test_case0 = [[1, 2, 3],
                  [4, 5, 6],
                  [0, 7, 8]]

    test_case1 = [[1, 2, 3],
                  [5, 0, 6],
                  [4, 7, 8]]

    test_case2 = [[1, 3, 6],
                  [5, 0, 2],
                  [4, 7, 8]]

    test_case3 = [[1,3,6],
                [5,0,7],
                [4,8,2]]

    test_case4 = [[1,6,7],
                [5,0,3],
                [4,8,2]]

    test_case5 = [[7,1,2],
                [4,8,5],
                [6,3,0]]

    test_case6 = [[0,7,2],
                [4,6,1],
                [3,5,8]]

    test_case7 = [[1,2,3,4],
                [5,6,7,8],
                [9,10,11,12],
                [13,0,14,15]]

    default_case_list = [test_case0,test_case1,test_case2,test_case3,test_case4,test_case5,test_case6,test_case7]

    return default_case_list[case_id]

if __name__ == '__main__':

    input_state = []

    print(" Type '1' to choice a default puzzle, or '2' to enter your own state.")
    choice1 = int(input())
    if choice1 == 1:
        print("default case:")
        for i in range(8):
            print(i+1)
            for j in range(len(default_case(i))):
                print(default_case(i)[j])
        print('Type case number (1-8): ')
        input_state = default_case(int(input())-1)
    else:
        print('Enter your puzzle, using a zero to represent the blank (bigger than 3*3 is OK! ):')
        print('Enter the 1 -th row : ',end='')
        first_row = list(map(int,input().split(' ')))
        input_state.append(first_row)
        for i in range(len(first_row)-1):
            print("Enter the", i+2 ,"-th row : ",end='' )
            curr_row = list(map(int,input().split(' ')))
            input_state.append(curr_row)



    n = len(input_state)
    goal = generate_goal(n)

    state_queue = [input_state]
    state_queue_set = {str(input_state)}
    parent_node = [-1]


    # state_queue.append(test_case2)
    state_index_queue = []

    # strategy choice
    print("Select algorithm. Type '0' for Uniform Cost Search, Type '1' for the Misplaced Tile Heuristic, or type '2' the Manhattan Distance Heuristic:")
    strategy_num = int(input())
    if strategy_num == 0:
        curr_strategy = uniform_cost_serch
    elif strategy_num == 1:
        curr_strategy = misplaced_heuristics
    else:
        curr_strategy = manhattan_heuristics

    # h is the estimated distance to the goal.
    h = curr_strategy(state_queue[0])

    # g is the cost to get to a state, it is equal to the depth.
    g = 0

    #We can think of f as the estimated cost of the cheapest solution that goes through this state
    f=g+h

    # add the f,g, state index into the minimum heap
    heapq.heappush(state_index_queue,[f,g,0])

    result = 0
    total_state_num = 0
    while state_index_queue:
        curr = heapq.heappop(state_index_queue)
        curr_state_index = copy.copy(curr[2])
        curr_depth = copy.copy(curr[1])
        curr_state = copy.deepcopy(state_queue[curr_state_index])


        for dirc in ['right','down','up','left']:
            curr_state_copy = copy.deepcopy(curr_state)
            next_state = blank_move_direction(curr_state_copy,dirc)

            # if the blank cannot move in this direction we need skip this state
            if next_state is None :
                continue

            # if this state is same as one of before states, skip this state
            if str(next_state) in state_queue_set:
                continue

            parent_index = curr_state_index
            state_queue.append(next_state)
            state_queue_set.add(str(next_state))

            # calculate the total number of states
            total_state_num += 1
            # print('total state numbers: ' , total_state_num)

            parent_node.append(parent_index)
            next_state_index = len(state_queue) - 1
            h = curr_strategy(next_state)
            g = curr_depth + 1
            f = g + h
            heapq.heappush(state_index_queue,[f,g,next_state_index])

            # if we find the goal, search stop.
            if next_state == goal:
                result = 1
                # move_step.append(next_state_index)
                break

        # print('total state numbers: ' , total_state_num)
        # the goal is be found, search stop
        if result == 1:
            break



    print_queue = []
    if result == 1:
        i = -1
        while parent_node[i] >= 0:
            print_queue.append(i)
            i = parent_node[i]
        print_queue.reverse()

        print_num = 0
        for i in print_queue:
            print_num += 1
            print('')
            print(print_num," h(n)=",curr_strategy(state_queue[i]))
            for j in range(n):
                print(state_queue[i][j])

    else :
        print("No solution")

    print("Solution depth is",g)
    print("Number of nodes expanded:",total_state_num)

    # print(h)
