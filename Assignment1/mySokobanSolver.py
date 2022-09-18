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
import multiprocessing
import os


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
    """

    Parameters
    ----------
    pos1 : tuple
        Start position (x1, y1).
    pos2 : tuple
        End positon (x2, y2).

    Returns
    -------
    int
        The value of the manhatten distance.

    """

    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def move(pos, movement):
    """

    Parameters
    ----------
    pos : tuple
        Start position (x, y).
    movement : tuple
        Translation vector that moves start position in given direction.

    Returns
    -------
    tuple
        The destination after moving from the start position.

    """
    
    return (pos[0] + movement[0], pos[1] + movement[1])

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
        self.initial = warehouse.worker, tuple(warehouse.boxes)
        self.weights = warehouse.weights
        self.goal = warehouse.targets
        self.boxes = warehouse.boxes
        self.walls = warehouse.walls

    def actions(self, state):
        """
        Return the list of legal actions that can be executed in the given state.

        """
        pos = state[0]
        boxes = list(state[1])
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
        """
        returns TRUE if all the boxes has reached a goal state, otherwise FALSE
        """
        return set(self.goal) == set(state[1])

    def path_cost(self, c, state1, action, state2):

        """
        returns cost from state1 to state2, where c is cost up to state1.
        """
        worker2 = state2[0]
        boxes1 = state1[1]
        boxes2 = state2[1]
       
        if boxes1 != boxes2:
            i = boxes1.index(worker2)
            box_cost = self.weights[i]
            return c + box_cost + 1
        else:
            return c + 1
        

    def h(self, n):
        '''
        The value of the heurtistic Manhattan Distance.
        
        Returns the sum of the manhattan distance of 
        each box to it's nearest target and worker to each box.
        '''

        worker = n.state[0]
        boxes = list(n.state[1])
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
        boxes = list(state[1])
         
        coord = direction.get(action)

        next_worker = move(worker, coord)
        
        if next_worker in boxes:
            next_box = move(next_worker, coord)
            i = boxes.index(next_worker)
            boxes[i] = next_box
        
        return next_worker, tuple(boxes)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



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
            
            next_worker = move(worker, coord)
            
            if next_worker in warehouse.walls:
                return 'Impossible'
            elif next_worker in warehouse.boxes:
                next_box = move(next_worker, coord)
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

# TEST

def test_check_elem_action_seq():
    """
    Test for check_elem_action_seq() from sanity_check.py.
    Testing two cases.
    """
    wh = sokoban.Warehouse()
    wh.load_warehouse("./warehouses/warehouse_01.txt")
    # first test
    answer = check_elem_action_seq(wh, ['Right', 'Right','Down'])
    expected_answer = '####  \n# .#  \n#  ###\n#*   #\n#  $@#\n#  ###\n####  '
    print('<<  check_elem_action_seq, test 1>>')
    if answer==expected_answer:
        print('Test 1 passed!  :-)\n')
    else:
        print('Test 1 failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    # second test
    answer = check_elem_action_seq(wh, ['Right', 'Right','Right'])
    expected_answer = 'Impossible'
    print('<<  check_elem_action_seq, test 2>>')
    if answer==expected_answer:
        print('Test 2 passed!  :-)\n')
    else:
        print('Test 2 failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)

def test_solve_weighted_sokoban(filename, expected_answer,  expected_cost):
    
    """
    Test for solve_weighted_sokoban() from sanity_check.py.
    """
    
    wh = sokoban.Warehouse()    
    wh.load_warehouse( "./warehouses/"+ filename)
    # first test
    t0 = time.time()
    answer, cost = solve_weighted_sokoban(wh)
    t1 = time.time()
     
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
    print(f'Solver took {t1-t0} seconds')
    
           
    


def test_actions():
   ''' 
   Test to see if worker pushes two boxes, should not be possible.
   The only possibe action should be 'Up'.
   '''
   wh = sokoban.Warehouse()
   wh.load_warehouse("./warehouses/warehouse_09.txt")
   s = SokobanPuzzle(wh)  
    
   answer = s.actions(s.initial)
   expected_answer = ['Up']
   print('<<  test_actions >>')
   if answer==expected_answer:
       print(' Answer as expected!  :-)\n')
   else:
       print('unexpected answer!  :-(\n')
       print('Expected ');print(expected_answer)
       print('But, received ');print(answer)
       
       

def test_result(): 
   '''
   Test to see if worker moves 'Down' and pushes box.
   Inital value for worker and box is (6,1) and (6,2).
   The y-value for both worker and box should increment by 1 .

   '''
   wh = sokoban.Warehouse()
   wh.load_warehouse("./warehouses/warehouse_15.txt")
   s = SokobanPuzzle(wh)  
    
   answer = s.result(s.initial, 'Down')
   expected_answer = (6,2), ((6,3), (5,4))
   print('<< test_result >>')
   if answer==expected_answer:
       print(' Answer as expected!  :-)\n')
   else:
       print('unexpected answer!  :-(\n')
       print('Expected ');print(expected_answer)
       print('But, received ');print(answer)
       

# Under is test_all() and the auxiliary function warehouse_solution(warehouse_problem).
# These can be commented out to create a csv-file over all the warehouses
# solved under two minutes, and a text-file of the remaining unfinished warehouses.

       
# def warehouse_solution(warehouse_problem):
#     """
#     Loop all warehouses in the test folder, and output the results to txt and csv file
#     """
#     with open(warehouse_problem) as f:
#         first_line = f.readline()
#     boxes = first_line.split(" ")
#     head, problem_file = os.path.split(warehouse_problem)
#     t0 = time.time()
#     wh = sokoban.Warehouse()
#     wh.load_warehouse(warehouse_problem)
#     solution, cost = solve_weighted_sokoban(wh)
#     t1 = time.time()

#     with open("./solutions/overall.csv", "a+") as file:
#         file.write(problem_file+", {}, {}, {}\n".format(t1-t0, cost, len(boxes)))
#         file.close()

        
# def test_all():
#     """
#     Test for solve_weighted_sokoban()
#     Testing for all warehouses by Automatic Timeout"""

#     directory = "./warehouses"

#     counts = 1

#     with open("./solutions/overall.csv", "a+") as file:
#         file.write("case,time,cost,boxes\n")
#         file.close()

#     for filename in os.listdir(directory):
#         f = os.path.join(directory, filename)
        
#         if f.endswith(".txt"):
#             print("Start test case " + filename +  " in {} of 108".format(counts))
#             p = multiprocessing.Process(target=warehouse_solution, args=(f,))
#             p.start()

#             # Wait for 300 seconds or until process finishes
#             p.join(120)

#             if p.is_alive():
#                 with open("./solutions/outtime.txt", 'a+') as file:
#                     file.write(filename+"\n")
#                     file.close()
#                 print("Test case {} is timeout.".format(counts))
#                 # Terminate - may not work if process is stuck for good
#                 p.terminate()
#                 # OR Kill - will work for sure, no chance for process to finish nicely however
#                 # p.kill()
            
#             counts += 1
            
#         else:
#             continue
    
#     print("Finish All Tests")
   
    

if __name__ == "__main__":

    print(my_team())  # should print your team
    print("---------------------")
    
    test_check_elem_action_seq()
    print("---------------------")
    
    test_actions()
    print("---------------------")
    
    test_result()
    print("---------------------")
    
    print("test - warehouse_8a:")
    test_solve_weighted_sokoban("warehouse_8a.txt", 
                                ['Up', 'Left', 'Up', 'Left', 'Left', 'Down', 
                                 'Left', 'Down', 'Right', 'Right', 'Right', 
                                 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 
                                 'Left', 'Left', 'Right', 'Right', 'Right', 
                                 'Right', 'Right', 'Right', 'Right'], 431)
    
    print("---------------------")
    print("test - warehouse_09:")
    test_solve_weighted_sokoban("warehouse_09.txt", 
                                ['Up', 'Right', 'Right', 'Down', 'Up', 'Left', 
                                 'Left', 'Down', 'Right', 'Down', 'Right', 
                                 'Left', 'Up', 'Up', 'Right', 'Down', 'Right',
                                 'Down', 'Down', 'Left', 'Up', 'Right', 'Up', 
                                 'Left', 'Down', 'Left', 'Up', 'Right', 'Up', 
                                 'Left'], 396)
    print("---------------------")
    print("test - warehouse_47:")
    test_solve_weighted_sokoban("warehouse_47.txt", 
                                ['Right', 'Right', 'Right', 'Up', 'Up', 'Up', 
                                 'Left', 'Left', 'Down', 'Right', 'Right', 
                                 'Down', 'Down', 'Left', 'Left', 'Left', 
                                 'Left', 'Up', 'Up', 'Right', 'Right', 'Up', 
                                 'Right', 'Right', 'Right', 'Right', 'Down', 
                                 'Left', 'Up', 'Left', 'Down', 'Down', 'Up', 
                                 'Up', 'Left', 'Left', 'Down', 'Left', 'Left', 
                                 'Down', 'Down', 'Right', 'Right', 'Right', 
                                 'Right', 'Right', 'Right', 'Down', 'Right', 
                                 'Right', 'Up', 'Left','Left', 'Left', 'Left', 
                                 'Left', 'Left', 'Down', 'Left', 'Left', 'Up', 
                                 'Up', 'Up', 'Right', 'Right', 'Right', 'Up', 
                                 'Right', 'Down', 'Down', 'Up', 'Left', 'Left', 
                                 'Left', 'Left', 'Down', 'Down', 'Down', 
                                 'Right', 'Right', 'Up', 'Right', 'Right', 
                                 'Left', 'Left', 'Down', 'Left', 'Left', 'Up', 
                                 'Right', 'Right'] , 179)
    print("---------------------")
    print("test - warehouse_81:")
    test_solve_weighted_sokoban("warehouse_81.txt", 
                                ['Left', 'Up', 'Up', 'Up', 'Right', 'Right', 
                                  'Down', 'Left', 'Down', 'Left', 'Down', 
                                  'Down', 'Down', 'Right', 'Right', 'Up', 
                                  'Left', 'Down', 'Left', 'Up', 'Right', 'Up', 
                                  'Up', 'Left', 'Left', 'Down', 'Right', 'Up', 
                                  'Right', 'Up', 'Right', 'Up', 'Up', 'Left', 
                                  'Left', 'Down', 'Down', 'Right', 'Down', 
                                  'Down', 'Left', 'Down', 'Down', 'Right', 'Up', 
                                  'Up', 'Up', 'Down', 'Left', 'Left', 'Up', 
                                  'Right']  , 376)
    print("---------------------")
    # print("test - all warehouses")
    # test_all()
    # print("---------------------")
    