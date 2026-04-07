
''' this is just a testfile remove later '''

from database.db_manager import db_function as db


import Generator as gen
from copy import deepcopy 





states = gen.GenerateSudokuSet(6, RNG=3)
initial  = deepcopy(states[0])
curr     = deepcopy(states[0]) 
solution = deepcopy(states[1])
new_id = db.add_new_map(initial,solution,40)
new_session = db.update_time(40,79.00)

print(new_id)
print(new_session)


'''
print(db.get_completed_sessions())




#code goes here          # TODO
        # Stop timer
        # Save metadata to DB

        ##FUNCITONS WE NEED DONE
#####TODO: FINISH THE SAVE SESION FUNCTIONS
#### TODO: RUN SESSION aka pull a session id from list and then call that session info from the db


from database.db_manager import db_function as db
from Game import Sudokugame as sg

print(db.get_completed_sessions())


def newgame():
    newgame = sg()
    return newgame
    

def previousgame(id):
    session_map = db.get_session_id_and_map(id)
    solution = db.get_solution_and_id(id)
    initial = db.get_initial_map(id)
    notes = db.get_notes(id)
    previous_session = sg(initial, session_map, solution,notes)
    return previous_session




###plese pick on of the two idk what ones you want
    
#when button pressed run get all sessions
def get_all_sessions_ids():
   allsessions =  db.get_all_sessions_ids()
   #hopefully all sesssions printed with indexes
   return allsessions



#idk if we want to get the completion status with the session id or not?
def get_all_sessions_complet():
   allsessions =  db.get_session_and_status() #returns back id and completion status

   return allsessions
#sessions[1][0] <-- for the id

sess = get_all_sessions_complet()
sessions = sess[1][0]
ipickthissession = sessions[1]

#call object game : D
previousgame(ipickthissession)



notes broke
   idk how to do this part help me
   but if selected_session call 
   previousgame(selected_session)
'''


####TODO: GET PREVIOUS SESSION LIST MAKE SURE THE STATUS IS THERE so a list of session_ids and their completion status
####TODO: generate new game needs to be it's own seperate functoin


'''
from bisect import insort # Used for inserting to lists in-order
from copy import deepcopy # Deepcopy the board since its nested lists
import numpy as np # Multi-dim arrays easily






matrix = [
    [[1,2,3,4], [1,2,3,4], [1,2,3,4]],
    [[1,2,3,4], [1,2,3,4], [1,2,3,4]],
    [[1,2,3,4], [1,2,3,4], [1,2,3,4]]
]

print("afterwords")
for row in matrix: print(" ".join(map(str, row)))

all_sessions = db.get_all_map_and_id()
map_ids = []
for row in all_sessions:
    map_ids.append(row[0])
print(map_ids)

sessions = db.get_session_id_and_map(1)  
session_id = []
for row in sessions:
    session_id.append(row[0])
print(session_id)


matrix = [
    [[1,2,3,4], [1,2,3,4], [1,2,3,4]],
    [[1,2,3,4], [1,2,3,4], [1,2,3,4]],
    [[1,2,3,4], [1,2,3,4], [1,2,3,4]]
]

print("afterwords")
for row in matrix: print(" ".join(map(str, row)))


db.update_notes(matrix)

notes = db.get_notes(1)
print("getback")
for row in notes: print(" ".join(map(str, row)))

matrix = db.convert_2d_to_3d(notes)
for row in matrix: print(" ".join(map(str, row)))


numEmpty = 20 # Set the number of empty cells
sudokuSet = Generator.GenerateSudokuSet(numEmpty)
new_map = db.array_to_string(sudokuSet[0])
solution = db.array_to_string(sudokuSet[1])


new_map_id = db.add_new_map(new_map,solution) #returns back it's id



solutionfromdb = db.get_solution_and_id(new_map_id)


print('from the db')
for row in mapfromdb[1]: print(" ".join(map(str, row)))
print('solution from db')
for row in solutionfromdb[1]: print(" ".join(map(str, row)))



print("Initial State")
for row in sudokuSet[0]: print(" ".join(map(str, row)))
new_map = db.array_to_string(sudokuSet[0])
print(new_map)
print("checkifconversionbackworks")
new_new_map = db.string_to_array(new_map)
for row in new_new_map: print(" ".join(map(str, row)))



print("Solution")
for row in sudokuSet[1]: print(" ".join(map(str, row)))
'''

#map = db

#print(map.get_all_map_and_id())

