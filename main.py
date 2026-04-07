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


'''
notes broke
   idk how to do this part help me
   but if selected_session call 
   previousgame(selected_session)
'''
