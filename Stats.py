
# Stats.py: Contains functions to graph stats of games in the DB

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from database.db_manager import db_function as db

# Return the completed sessions information for later statistics use
def completed_sessions():   
    # Get all the current sessions from the DB  
    all_sessions = db.get_all_map_and_id()
    completed = []

    # Loop through the sessions and gather all the completed sessions information 
    for row in all_sessions:
        map_id = row[0]
        sessions = db.get_session_id_and_map(map_id)  

        for session in sessions:
            session_id = session[0]
            status = db.get_completion_status(session_id)
            time = db.get_completion_time(session_id)
            errors = db.get_num_errors(session_id)
            difficulty = db.get_difficulty(session_id)

            if status == 1:
                completed.append({
                    "map_id": map_id,
                    "session_id": session_id,
                    "time_spent": time,
                    "number_of_errors": errors,
                    "map_difficulty": difficulty, 
                    "session_map": session[1]
                })

    return completed

def GamesByTime():
    """Graphs games by ID / Time (Chronological play order)"""
    completed = completed_sessions()
    if not completed:
        print("No completed sessions found.")
        return

    df = pd.DataFrame(completed)
    sns.scatterplot(x="session_id", y="time_spent", data=df, hue="time_spent")
    plt.title("Time Spent per Completed Session")
    plt.xlabel("Session ID")
    plt.ylabel("Time Spent")
    plt.show()

def ErrorRate(): 
    """Graphs the error rate based on the number of errors per completed game"""
    completed = completed_sessions()
    if not completed:
        print("No completed sessions found.")
        return

    df = pd.DataFrame(completed)
    sns.regplot(x="session_id", y="number_of_errors", data=df)
    plt.title("Errors Per Game")
    plt.xlabel("Session ID")
    plt.ylabel("Number Of Errors")
    plt.show()

def Difficulty():
    """Graphs the sessions into different groups of difficulty"""
    completed = completed_sessions()
    if not completed:
        print("No completed sessions found.")
        return

    df = pd.DataFrame(completed)
    plt.pie(df['session_id'].sum(), labels = df['map_difficulty'], autopct='%1.1f%%')
    plt.title("Difficulty")
    plt.xlabel("Difficulty")
    plt.ylabel("Sessions")
    plt.show()
 

GamesByTime()
ErrorRate()
Difficulty()