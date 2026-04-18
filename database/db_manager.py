### welcome to the db manager
### allows to fetch and update the sql database


###make the save to db functions in game still fix the 3d matrix issues

import sqlalchemy as db
import json

import logging

engine = engine = db.create_engine('sqlite:///database/pydoku.db')


logging.basicConfig(
    level=logging.INFO,
    filename='pydoku.log',
    filemode='a',
    format='%(asctime)s | %(name)-15s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S',
)

logger = logging.getLogger(f"{__name__}")

class db_function:
# converter functions
    def convert_3d_to_1d(matrix):
        flat_matrix = []
        #loop through the matrix and store it to a 1D list     
        for row in range(9):
            for column in range(9):
                for n in range(9):
                    flat_matrix.append(int(matrix[row][column][n]))
        return flat_matrix
    
    def convert_1d_to_3d(flat_matrix):
        matrix = [[[0 for _ in range(9)] for _ in range(9)] for _ in range(9)]
        i = 0
        #loop through the flat list and add the values to our 3D matrix  
        for row in range(9):
            for column in range(9):
                for n in range(9):
                    matrix[row][column][n] = flat_matrix[i]
                    i += 1
        return matrix 
                   
    def string_to_array(string_map):
        arr = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
        ]

        j=0
        e =0
        for i in range(81):
            if(i%9==0 and i != 0):
                j+=1
                e=0


            arr[j][e] = int(string_map[i])
            e+=1    
            

        return arr
    
    def array_to_string(array_map):
        new_string = ''

        for i in range(9):
            for j in range(9):
                new_string+= str(array_map[i][j])

        return new_string

    ####################### fetch functions
    def ID_exists(id) -> bool:
        '''Returns T/F if an entry with ID exists'''
        MAP = db.Table('MAP', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.map_id).where(MAP.c.map_id == id)
        result = engine.connect().execute(query).fetchall()

        return (result != None)

    #### from table map
    def get_all_map_and_id():
        MAP = db.Table('MAP', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.map_id,MAP.c.map)
        result = engine.connect().execute(query).fetchall()
        '''
        result = get_map_by_id(1,get_connection()) #return id and the map
        print(result[0][1]) #<-- should print only the map
        print(result[1][0]) <-- for the id
        '''
        return result

    def get_initial_map(ses_id):
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.map_id).where(MAP.columns.session_id == ses_id)

        map_id = engine.connect().execute(query).fetchall()
        query = db.select(MAP.c.map).where(MAP.columns.session_id == map_id)

        result= engine.connect().execute(query).fetchall()
        return result

    def get_map_and_id(id):
        MAP = db.Table('MAP', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.map_id,MAP.c.map).where(MAP.c.map_id == id)

        result = engine.connect().execute(query).fetchall()

        '''
        result = get_map_by_id(1,get_connection()) #return id and the map
        print(result[0][1]) #<-- should print only the map
        print(result[1][0]) <-- for the id
        '''
        return result

    def get_completed_howmanytimes(id):
        MAP = db.Table('MAP', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.completed_howmanytimes).where(MAP.c.map_id == id)

        result = engine.connect().execute(query).scalar()

        print(result)
        return result

    def get_difficulty(id):
        MAP = db.Table('MAP', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.difficulty).where(MAP.columns.map_id == id)

        result = engine.connect().execute(query).scalar()

        return result

    ########## MAP SOLUTIONS ARE HERE
    def get_solution_and_id(id):
        MAP = db.Table('MAP_SOLUTIONS', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.map_id,MAP.c.map_solution).where(MAP.columns.map_id == id)

        result = engine.connect().execute(query).fetchall()


        return result

    ###########FUNCTIONS FOR THE SESSION ARE HERE

    def get_completed_sessions():
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.session_id,MAP.c.session_map).where(MAP.columns.completion_status == 1)

        result = engine.connect().execute(query).fetchall()
        return result

    def get_session_and_status():
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.session_id,MAP.c.completion_status)

        result = engine.connect().execute(query).fetchall()
        return result

    def get_all_sessions_ids():
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.session_id)

        result = engine.connect().execute(query).fetchall()
        return result

    def get_session_id_and_map(id):
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.session_id,MAP.c.session_map).where(MAP.columns.map_id == id)

        result = engine.connect().execute(query).fetchall()
        return result

    def get_one_session_id_and_map(ses_id):
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.session_id,MAP.c.session_map).where(MAP.columns.session_id == ses_id)

        result = engine.connect().execute(query).fetchall()

        return result

    def get_all_sessions():
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.session_id,MAP.c.session_map)

        result = engine.connect().execute(query).fetchall()

        return result

    def get_completion_time(id):
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.time_spent).where(MAP.columns.session_id == id)

        result = engine.connect().execute(query).scalar()

        return result

    def get_completion_status(id):
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.completion_status).where(MAP.columns.session_id == id)

        result = engine.connect().execute(query).scalar()

        return result

    def get_notes(id):
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.notes).where(MAP.c.session_id == id)

        result = engine.connect().execute(query).scalar()

        if result is None:
            return None  
        
        notes_flat = json.loads(result)
        notes_3d = db_function.convert_1d_to_3d(notes_flat)

        return notes_3d

    def get_num_errors(id):
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.num_errors).where(MAP.columns.session_id == id)

        result = engine.connect().execute(query).scalar()

        return result

    ############# insert rows into  tables

    def add_solution(id,solution_string):
        MAP = db.Table('MAP_SOLUTIONS', db.MetaData(), autoload_with=engine)
        conn = engine.connect()

        insert_query = MAP.insert().values(map_id=id,map_solution = solution_string)
        conn.execute(insert_query)
        conn.commit()

    def add_new_map(map_array,solution_array,diffi):
        MAP = db.Table('MAP', db.MetaData(), autoload_with=engine)
        conn = engine.connect()

        query = db.select(db.func.max(MAP.c.map_id))
        map_ids = conn.execute(query).scalar()
        new_id = map_ids  + 1
        map_array = db_function.array_to_string(map_array)
        solution_array = db_function.array_to_string(solution_array)

        insert_query = MAP.insert().values(map_id=new_id,completed_howmanytimes=None,map=map_array, difficulty = diffi)
        conn.execute(insert_query)
        conn.commit()
        db_function.add_solution(new_id,solution_array)

        return new_id

    def add_session(id,sess_map,):
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)
        conn = engine.connect()
        
        sess_map_str = db_function.array_to_string(sess_map)
        query = db.select(db.func.max(MAP.c.session_id))
        map_ids = conn.execute(query).scalar()
        new_id = map_ids  + 1 
        
        insert_query = MAP.insert().values(map_id=id,session_id = new_id, completion_status = 0,session_map=sess_map_str)
        conn.execute(insert_query)
        conn.commit()

    #delete rows in the table
    def delete_map(id):
        MAP = db.Table('MAP', db.MetaData(), autoload_with=engine)
        conn = engine.connect()

        query = MAP.delete().where(MAP.c.map_id == id)

        conn.execute(query)
        conn.commit()

        db_function.delete_solution(id)

    def delete_solution(id):
        MAP = db.Table('MAP_SOLUTIONS', db.MetaData(), autoload_with=engine)
        conn = engine.connect()

        query = MAP.delete().where(MAP.c.map_id == id)

        conn.execute(query)
        conn.commit()

    def delete_session(id):
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)

        conn = engine.connect()

        query = MAP.delete().where(MAP.c.session_id == id)

        conn.execute(query)
        conn.commit()

    ############### update into tables
    #update the map

    def update_difficulty(diffi,id):
        MAP = db.Table('MAP', db.MetaData(), autoload_with=engine)
        conn = engine.connect()


        query = db.update(MAP).where(MAP.c.map_id == id).values(difficulty = diffi)
        conn.execute(query)
        conn.commit()

    def update_completed_howmanytimes(id):
        MAP = db.Table('MAP', db.MetaData(), autoload_with=engine)
        conn = engine.connect()

        query = db.select(db.func.max(MAP.c.completed_howmanytimes))
        nbruh = conn.execute(query).scalar()
        if(nbruh):
            newval = int(nbruh) +1
        else:
            newval = 1 # > ; P

        query = db.update(MAP).where(MAP.c.map_id == id).values(completed_howmanytimes=newval)
        conn.execute(query)
        conn.commit()

    #update values in session
    def update_notes(note):
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)
        conn = engine.connect()
        
        notes = db_function.convert_3d_to_1d(note)
        notes_json = json.dumps(notes)

        query = db.update(MAP).where(MAP.c.session_id == 1).values(notes = notes_json)
        conn.execute(query)
        conn.commit()

    def save_session(sess_id, new_session_map, timestamp, notes):
        #converted session map to str 

        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)
        conn = engine.connect()
        notes_flat = db_function.convert_3d_to_1d(notes)
        notes_json = json.dumps(notes_flat)
        session_map_str = db_function.array_to_string(new_session_map)
        ttimestamp = float(timestamp)
        
        query = db.update(MAP).where(MAP.c.session_id == sess_id).values(time_spent = ttimestamp, session_map = session_map_str, notes = notes_json)
        conn.execute(query)
        conn.commit()

    def update_time(sess_id,time):

        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)
        conn = engine.connect()
        ttimestamp = float(time)

        query = db.update(MAP).where(MAP.c.session_id == sess_id).values(time_spent = ttimestamp)
        conn.execute(query)
        conn.commit()

    def update_completion_status(ses_id,completionstatus):
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)
        conn = engine.connect()

        if completionstatus == 0:
            query = db.update(MAP).where(MAP.c.session_id == ses_id).values(completion_status = 0)
        else:
            query = db.update(MAP).where(MAP.c.session_id == ses_id).values(completion_status = 1)
        conn.execute(query)
        conn.commit()

    def update_num_errors(newerror,ses_id):
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)
        conn = engine.connect()


        query = db.update(MAP).where(MAP.c.session_id == ses_id).values(num_errors = newerror)
        conn.execute(query)
        conn.commit()

    def load_prev_game():
        SESSION = db.Table('SESSION', db.MetaData(), autoload_with= engine)
        MAP = db.Table('MAP', db.MetaData(), autoload_with= engine)
        SOL = db.Table('MAP_SOLUTIONS', db.MetaData(), autoload_with= engine)
        conn = engine.connect()

        #try to get the last incomplete game
        query = db.select(SESSION).where(SESSION.c.completion_status == 0).order_by(SESSION.c.session_id.desc())
        result = conn.execute(query).fetchone()

        #if theres none, get the last one completed
        if not result:
            query = db.select(SESSION).order_by(SESSION.c.session_id.desc())
            result = conn.execute(query).fetchone()

        #if neither exists, return none
        if not result:
           return None  

        session_id = result.session_id
        map_id = result.map_id

        #get the map and its solution
        map_query = db.select(MAP.c.map).where(MAP.c.map_id == map_id)
        sol_query = db.select(SOL.c.map_solution).where(SOL.c.map_id == map_id)

        map_str = conn.execute(map_query).scalar()
        sol_str = conn.execute(sol_query).scalar()

        #convert everything
        curr = db_function.string_to_array(result.session_map)
        initial = db_function.string_to_array(map_str)
        solution = db_function.string_to_array(sol_str)

        notes = None
        if result.notes:
            notes_flat = json.loads(result.notes)
            notes = db_function.convert_1d_to_3d(notes_flat)

        return {
            "session_id": session_id,
            "initial": initial,
            "curr": curr,
            "solution": solution,
            "notes": notes,
            "time": result.time_spent if result.time_spent is not None else 0.0,
            "difficulty": db_function.get_difficulty(map_id)
        }
        
    def get_all_sessions_for_select():
        SESSION = db.Table('SESSION', db.MetaData(), autoload_with=engine)
        conn = engine.connect()
        
        # Get me all of the game sessions and statuses so I can acess them.
        q = db.select(
            SESSION.c.session_id, 
            SESSION.c.map_id, 
            SESSION.c.time_spent, 
            SESSION.c.completion_status
        ).order_by(SESSION.c.session_id.desc())
        
        return conn.execute(q).fetchall()
    