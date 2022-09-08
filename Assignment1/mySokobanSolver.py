"""

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2022-03-27  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

"""

# You have to make sure that your code works with
# the files provided (search.py and sokoban.py) as your code will be tested
# with these files
import search
import sokoban
import time


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    """
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)

    """
    return [(11385081, "Sinan", "Maric"), (11385049, "Mads Olav", "Eek")]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

direction = {
     "Left": (-1, 0),
     "Right": (1, 0),
     "Up": (0, -1),
     "Down": (0, 1),
 }  # (x,y) = (column,row)

def manhattan_distance(pos1, pos2):

    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# state - position of worker and boxes (dynamic)


class SokobanPuzzle(search.Problem):
    """
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of
    the provided module 'search.py'.

    """

    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to
    #     complete this class. For example, a 'result' method is needed
    #     to satisfy the interface of 'search.Problem'.
    #
    #     You are allowed (and encouraged) to use auxiliary functions and classes

    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.initial = warehouse.worker, warehouse.boxes[0], warehouse.boxes[1]
        self.weights = warehouse.weights
        self.goal = warehouse.targets
        self.boxes = warehouse.boxes
        self.walls = warehouse.walls

    def actions(self, state):
        """
        Return the list of legal actions that can be executed in the given state.

        """
        pos = state[0]
        box1 = state[1]
        box2 = state[2]
        boxes = [box1, box2]
        L = []


        for d in direction:
            coord = direction.get(d)
            x = coord[0]
            y = coord[1]
            next_pos = (pos[0] + x, pos[1] + y)
            if next_pos in self.walls:
                continue
            
            if next_pos in boxes:
                next_box_pos = (next_pos[0] + x, next_pos[1] + y)
                if next_box_pos not in self.walls and next_box_pos not in boxes:
                    L.append(d)
            else:
                L.append(d)
            

        return L
    
    def goal_test(self, state):
        return set(self.goal) == set([state[1], state[2]])

    def path_cost(self, c, state1, action, state2):

        """
        returns cost from state1 to state2, where c is cost up to state1.
        """
        worker2 = state2[0]
        boxes1 = [state1[1], state1[2]]
        boxes2 = [state2[1], state2[2]]
        if boxes1 != boxes2:
            i = boxes1.index(worker2)
            box_cost = self.weights[i]
            return c + box_cost + 1
        else:
            return c + 1
        

    def h(self, n):

        worker = n.state[0]
        boxes = [n.state[1], n.state[2]]
        targets = self.goal
        weights = self.weights

        heuristic = 0

        for i, box in enumerate(boxes):
            min_dist = float("inf")
            worker_box_distance = manhattan_distance(box, worker)
            for target in targets:
                dist = manhattan_distance(box, target) * (
                    1 + weights[i]
                )
                if dist <= min_dist:
                    min_dist = dist
            heuristic += worker_box_distance + min_dist
        return heuristic

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        
        worker = state[0]
        boxes = [state[1], state[2]]
         
        coord = direction.get(action)
        x = coord[0]
        y = coord[1]
        next_worker = (worker[0] + x, worker[1] + y)
        
        if next_worker in boxes:
            next_box = (next_worker[0] + x, next_worker[1] + y)
            i = boxes.index(next_worker)
            boxes[i] = next_box
        
        return next_worker, boxes[0], boxes[1]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -




# def check_action(position, warehouse, action):
#     '''
#     Checking if action is impossible, if not applies action.

#     @param warehous: a valid Warehouse object

#     @param action: a string representing an action.
#             For example, 'Left'.

#     @return
#         The string 'Impossible', if the action is not valid.
#            For example, if the agent tries to push two boxes at the same time,
#                         or push a box into a wall.
#         Otherwise, if the action is succesful, the action is applied.
#     '''

#     pos = position
#     new_pos = (pos[0] + move(action)[0], pos[1] + move(action)[1])


#     #checking if worker hits a wall
#     if new_pos in warehouse.walls:
#         return 'Impossible'
#     elif new_pos in warehouse.boxes:
#         new_box_pos = (new_pos[0] + move(action)[0], new_pos[1] + move(action)[1])
#         if new_box_pos not in warehouse.boxes and new_box_pos not in warehouse.boxes:
#             warehouse.boxes.remove(new_pos)
#             warehouse.boxes.append(new_box_pos)
#             pos = new_pos
#         else:
#             return 'Impossible'
#     else:
#         pos = new_pos
#     return pos
#     print(warehouse.worker)


def check_elem_action_seq(warehouse, action_seq):
    """

    Determine if the sequence of actions listed in 'action_seq' is legal or not.

    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.

    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']

    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    """

    ##         "INSERT YOUR CODE HERE"
    
    for action in action_seq:
        worker = warehouse.worker
        if action in list(direction.keys()):
            coord = direction.get(action)
            x = coord[0]
            y = coord[1]
            
            next_worker = (worker[0] + x, worker[1] + y)
            
            if next_worker in warehouse.walls:
                return 'Impossible'
            elif next_worker in warehouse.boxes:
                next_box = (next_worker[0] + x, next_worker[1] + y)
                if next_box in warehouse.walls or next_box in warehouse.boxes:
                    return 'Impossible'
                else:
                    i = warehouse.boxes.index(next_worker)
                    warehouse.boxes[i] = next_box
            else:
                warehouse.worker = next_worker
    return warehouse.__str__()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def solve_weighted_sokoban(warehouse):
    """
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution.
    The second item is the total cost of this action sequence.

    @param
     warehouse: a valid Warehouse object

    @return

        If puzzle cannot be solved
            return 'Impossible', None

        If a solution was found,
            return S, C
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    """

    mySokoban = SokobanPuzzle(warehouse)

    solution = search.astar_graph_search(mySokoban)

    if solution is None:
        return "Impossible", None
    else:
        S = solution.solution()
        C = solution.path_cost
    return S, C


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def test_solve_weighted_sokoban():
    wh = sokoban.Warehouse()    
    wh.load_warehouse( "./warehouses/warehouse_81.txt")
    # first test
    answer, cost = solve_weighted_sokoban(wh)

    expected_answer = ['Up', 'Left', 'Up', 'Left', 'Left', 'Down', 'Left', 
                       'Down', 'Right', 'Right', 'Right', 'Up', 'Up', 'Left', 
                       'Down', 'Right', 'Down', 'Left', 'Left', 'Right', 
                       'Right', 'Right', 'Right', 'Right', 'Right', 'Right'] 
    expected_cost = 431
    print('<<  test_solve_weighted_sokoban >>')
    if answer==expected_answer:
        print(' Answer as expected!  :-)\n')
    else:
        print('unexpected answer!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
        print('Your answer is different but it might still be correct')
        print('Check that you pushed the right box onto the left target!')
    print(f'Your cost = {cost}, expected cost = {expected_cost}')
        
    

if __name__ == "__main__":
    pass    
#    print(my_team())  # should print your team
    t0 = time.time()
    test_solve_weighted_sokoban()
    t1 = time.time()
    
    print ("Solver took ",t1-t0, ' seconds')