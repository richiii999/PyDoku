'''
class DB_Manager:
let todo is add the engine value as a defaulted value in class constructor thing
'''


import sqlalchemy as db

# GENERIC STUFF
def get_connection():
    engine = db.create_engine('sqlite:///pydoku.db')
    return engine
engine = get_connection()




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
            new_string+= array_map[i][j]

    return new_string

'''
bluh = string_to_array('000601005000000890630508024500016200900000000000302000100000080200030000090405000')

print(bluh)
print(array_to_string(bluh))
'''


####################### fetch functions

#### from table map
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
def get_map_solution_and_id(id):
    MAP = db.Table('MAP_SOLUTIONS', db.MetaData(), autoload_with=engine)

    query = db.select(MAP.c.map_id,MAP.c.map).where(MAP.columns.map_id == id)

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

    query = db.select(MAP.c.time_spent).where(MAP.columns.sesion_id == id)

    result = engine.connect().execute(query).scalar()

    return result

def get_completion_status(id):
    MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)

    query = db.select(MAP.c.completion_status).where(MAP.columns.sesion_id == id)

    result = engine.connect().execute(query).scalar()

    return result


############# inser into  tables
def add_new_map(map_string):
    MAP = db.Table('MAP', db.MetaData(), autoload_with=engine)
    conn = engine.connect()
    
    query = db.select(db.func.max(MAP.c.map_id))
    map_ids = conn.execute(query).scalar()
    new_id = map_ids  + 1 
    
    insert_query = MAP.insert().values(map_id=new_id,completed_howmanytimes=None,map=map_string )
    conn.execute(insert_query)
    conn.commit()
    
def add_solution(id,solution_string):
    MAP = db.Table('MAP_SOLUTIONS', db.MetaData(), autoload_with=engine)
    conn = engine.connect()
    
    insert_query = MAP.insert().values(map_id=id,map_solution = solution_string)
    conn.execute(insert_query)
    conn.commit()

def add_session(id,sess_map,):
    MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)
    conn = engine.connect()
    
    query = db.select(db.func.max(MAP.c.session_id))
    map_ids = conn.execute(query).scalar()
    new_id = map_ids  + 1 
    
    insert_query = MAP.insert().values(map_id=id,session_id = new_id, completion_status = 0,session_map=sess_map)
    conn.execute(insert_query)
    conn.commit()



############### update into tables
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

def save_session(sess_id, new_session_map, timestamp):
    MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)
    conn = engine.connect()

    
    query = db.update(MAP).where(MAP.c.session_id == sess_id).values(time_spent = timestamp, session_map = new_session_map)
    conn.execute(query)
    conn.commit()

def update_session_completion_status(ses_id):
    MAP = db.Table('SESSION', db.MetaData(), autoload_with=engine)
    conn = engine.connect()

    
    query = db.update(MAP).where(MAP.c.session_id == ses_id).values(completion_status = 1)
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