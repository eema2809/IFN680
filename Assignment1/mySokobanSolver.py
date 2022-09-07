
'''

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

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban
import Math


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (11385081, 'Sinan', 'Maric'), (11385049, 'Mads Olav', 'Eek') ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# state - position of worker and boxes (dynamic)

class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
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
       

    def actions(self, state):
        """
        Return the list of legal actions that can be executed in the given state.
        
        """
        wh = self.warehouse
        pos = state[0]
        box1 = state[1]
        box2 = state[2]
        L = []
     
        direction = {'Left' :(-1,0), 'Right':(1,0) , 'Up':(0,-1), 'Down':(0,1)} # (x,y) = (column,row)
        
        for d in direction:
            coord = direction.get(d)
            x = coord[0]
            y = coord[1]
            new_pos = (pos[0] + x, pos[1] + y)
            #checking if worker hits a wall
            if new_pos == box1:
                new_box1 = (box1[0] + x, box1[1] + y)
                if (new_box1 != box2) and (new_box1 not in wh.walls):
                    L.append(d)
            elif new_pos == box2:
                new_box2 = (box2[0] + x, box2[1] + y)
                if (new_box2 != box1) and (new_box2 not in wh.walls):
                    L.append(d)
            elif new_pos not in wh.walls:
                L.append(d)
            
            
        return L
   
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        next_state = list(state)
        worker = next_state[0]
        box1 = next_state[1]
        box2 = next_state[2]
        
        if (worker[0]+move(action)[0], worker[1]+move(action)[1]) == box1:
            box1 = (box1[0]+move(action)[0], box1[1]+move(action)[1])
        elif (worker[0]+move(action)[0], worker[0]+move(action)[0]) == box2:
            box1 = (box2[0]+move(action)[0], box2[1]+move(action)[1])
        worker = (worker[0]+move(action)[0], worker[1]+move(action)[1])
        
        next_state = (worker, box1, box2)

        
        return next_state

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def move(action):
    '''
    Movement in coordiantes (x,y).
    
    @param action: a string representing an action.
            For example, 'Left'.
            
    @return
        The (x, y) coordinates for a given action.
            For example, if the action is 'Left' it returns (-1, 0)
    '''
    
    direction = {'Left' :(-1,0), 'Right':(1,0) , 'Up':(0,-1), 'Down':(0,1)} # (x,y) = (column,row)
    return direction[action]

def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key
 
    return "key doesn't exist"


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
    '''
    
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
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    
    sp = SokobanPuzzle(warehouse)
    state = [warehouse.worker, warehouse.boxes[0], warehouse.boxes[1]] #get state from warehouse
    L = sp.actions(state)

    print(state)
    print(L)
    
    for action in action_seq:
        if action in L:
            state = sp.result(state,action)
            print(state)
            L = sp.actions(state)
            print(L)
        else:
            return "Impossible"
    
           
        
    new_wh = warehouse.copy(state[0], (state[1], state[2]))
    print(warehouse.boxes)
    print(warehouse)
    print(new_wh.__str__())
    return new_wh.__str__()



def heur_manhattan_distance(warehouse, state):
    
    boxes = [state[1], state[2]]
    targets = warehouse.targets
    weights = warehouse.weights
    h = 0
    i = 0
   
    for box in boxes:
        min_dist = float("inf")
        for target in targets:           
            dist = (Math.abs(target[0] - box[0]) + Math.abs(target[1] - box[1])) * (1 + weights[i]) #is it correct distance function?
            if dist <= min_dist:
                min_dist = dist
        h += min_dist
        min_dist = float("inf")
        i+=1
    return h
        
            
        
    
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
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

    '''
    
        


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

