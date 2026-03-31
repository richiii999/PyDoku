### welcome to the db manager
### allows to fetch and update the sql database


## TODo:add new column for the notes 3d matrix for the session

import sqlalchemy as db
import json 

engine = engine = db.create_engine('sqlite:///database/pydoku.db')

class db_function:

# converter functions
    def convert_3d_to_2d(matrix):
        return [row for layer in matrix for row in layer]
    
    def convert_2d_to_3d(matrix_2d):
        return [
            matrix_2d[i:i + 9]
            for i in range(0, len(matrix_2d), 9)
        ]
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
            if(i%9==0 and i != 0): #there is a method to this madness
                j+=1
                e=0
                

            arr[j][e] = string_map[i]
            e+=1
            

        return arr
    def array_to_string(array_map):
        new_string = '' 

        for i in range(9):
            for j in range(9):
                new_string+= str(array_map[i][j])

        return new_string

    '''
    bluh = string_to_array('000601005000000890630508024500016200900000000000302000100000080200030000090405000')

    print(bluh)
    print(array_to_string(bluh))
    '''


    ####################### fetch functions

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

    ########## MAP SOLUTIONS ARE HERE
    def get_solution_and_id(id):
        MAP = db.Table('MAP_SOLUTIONS', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.map_id,MAP.c.map_solution).where(MAP.columns.map_id == id)

        result = engine.connect().execute(query).fetchall()

        '''
        result = get_map_by_id(1,get_connection()) #return id and the map
        print(result[0][1]) #should print only the map
        '''
        return result


    ###########FUNCTIONS FOR THE SESSION ARE HERE
    def get_session_id_and_map(id):
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)

        query = db.select(MAP.c.session_id,MAP.c.session_map).where(MAP.columns.map_id == id)

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
        
        notes_2d = json.loads(result)
        notes_3d = db_function.convert_2d_to_3d(notes_2d)

        return notes_3d

    ############# insert rows into  tables

    
    
    def add_solution(id,solution_string):
        MAP = db.Table('MAP_SOLUTIONS', db.MetaData(), autoload_with=engine)
        conn = engine.connect()
        
        insert_query = MAP.insert().values(map_id=id,map_solution = solution_string)
        conn.execute(insert_query)
        conn.commit()

    def add_new_map(map_string,solution_string):
        MAP = db.Table('MAP', db.MetaData(), autoload_with=engine)
        conn = engine.connect()
        
        query = db.select(db.func.max(MAP.c.map_id))
        map_ids = conn.execute(query).scalar()
        new_id = map_ids  + 1 
        
        insert_query = MAP.insert().values(map_id=new_id,completed_howmanytimes=None,map=map_string )
        conn.execute(insert_query)
        conn.commit()
        db_function.add_solution(new_id,solution_string)

        return new_id
    

    def add_session(id,sess_map,):
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)
        conn = engine.connect()
        
        query = db.select(db.func.max(MAP.c.session_id))
        map_ids = conn.execute(query).scalar()
        new_id = map_ids  + 1 
        
        insert_query = MAP.insert().values(map_id=id,session_id = new_id, completion_status = 0,session_map=sess_map)
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

    #update values in map
    def update_notes(note):
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)
        conn = engine.connect()
        
        notes = db_function.convert_3d_to_2d(note)
        notes_json = json.dumps(notes)
        
        query = db.update(MAP).where(MAP.c.session_id == 1).values(notes = notes_json)
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

    #update the session
    def save_session(sess_id, new_session_map, timestamp, notes):
        #needed is converting the 3d matrix(notes) into a 2d one and saving to the column sesion_notes

        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)
        conn = engine.connect()
        notes_2d = db_function.convert_3d_to_2d(notes)
        notes_json = json.dumps(notes_2d) 
        ttimestamp = float(timestamp)
        
        query = db.update(MAP).where(MAP.c.session_id == sess_id).values(time_spent = ttimestamp, session_map = new_session_map,notes = notes_json)
        conn.execute(query)
        conn.commit()

    def update_time(sess_id,time):

        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)
        conn = engine.connect()
        ttimestamp = float(time)
        
        query = db.update(MAP).where(MAP.c.session_id == sess_id).values(time_spent = ttimestamp)
        conn.execute(query)
        conn.commit()

    def update_completion_status_true(ses_id):
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)
        conn = engine.connect()

        
        query = db.update(MAP).where(MAP.c.session_id == ses_id).values(completion_status = 1)
        conn.execute(query)
        conn.commit()

    def update_completion_status_false(ses_id):
        MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)
        conn = engine.connect()

        
        query = db.update(MAP).where(MAP.c.session_id == ses_id).values(completion_status = 0)
        conn.execute(query)
        conn.commit()
    '''
    update_completed_howmanytimes(1)
    get_completed_howmanytimes(1)
    '''



    '''

    new_id = create_new_map('000601005000000890630508024500016200900000000000302000100000080200030000090405000')
    print(get_map_and_id(new_id))

    statement1 = books.insert().values(bookId=1, book_price=12.2,
                                    genre='fiction',
                                    book_name='Old age')
    '''



    '''
    db.select([films]).where(db.and_(films.columns.certification == 'R',
                                    films.columns.release_year > 2003))
                                    
    '''