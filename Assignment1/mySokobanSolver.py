
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
        self.state = (warehouse.worker, warehouse.boxes)

    def actions(self, state):
        """
        Return the list of legal actions that can be executed in the given state.
        
        """
        position = state[0]
        
        warehouse = self.warehouse
        
        L = []
     
        direction = {'Left' :(-1,0), 'Right':(1,0) , 'Up':(0,-1), 'Down':(0,1)} # (x,y) = (column,row)
        pos = state[0]
        pos_boxes = state[1]
        
        for key in direction:
            new_pos = (pos[0] + move(key)[0], pos[1] + move(key)[1])
            #checking if worker hits a wall
            if new_pos in pos_boxes:
                new_box_pos = (new_pos[0] + move(key)[0], new_pos[1] + move(key)[1])
                if new_box_pos not in pos_boxes and new_box_pos not in warehouse.walls:
                    state[1].remove(new_pos)
                    state[1].append(new_box_pos)
                    pos = new_pos
                    L.append(get_key(direction, move(key)))
                
            elif new_pos not in warehouse.walls:
                pos = new_pos
                L.append(get_key(direction, move(key)))
    
        return L
   
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        
        if action in self.actions(state):
            return state[0] + move(action)
        if action in self.actions(state) and state[0]+move(action) in state[1]:
            return state[1] + move(action)
        

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


def check_action(position, warehouse, action):
    '''
    Checking if action is impossible, if not applies action.
    
    @param warehous: a valid Warehouse object
    
    @param action: a string representing an action.
            For example, 'Left'.
    
    @return
        The string 'Impossible', if the action is not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if the action is succesful, the action is applied.
    '''
    
    pos = position
    new_pos = (pos[0] + move(action)[0], pos[1] + move(action)[1])
 
 
        
    #checking if worker hits a wall
    if new_pos in warehouse.walls:
        return 'Impossible'
    elif new_pos in warehouse.boxes:
        new_box_pos = (new_pos[0] + move(action)[0], new_pos[1] + move(action)[1])
        if new_box_pos not in warehouse.boxes and new_box_pos not in warehouse.boxes:
            warehouse.boxes.remove(new_pos)
            warehouse.boxes.append(new_box_pos)
            pos = new_pos
        else:
            return 'Impossible'
    else:
        pos = new_pos
    return pos
    print(warehouse.worker)
    

    

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
    
    
    new_wh = warehouse.copy(warehouse.worker, warehouse.boxes)
    sp = SokobanPuzzle(new_wh)
        
    for action in action_seq:
        if action in sp.actions(sp.state):
            sp.result(sp.state, action)
        else:
            return "Impossible"        
        
    return sp.warehouse.__str__()


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
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

