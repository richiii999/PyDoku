
# Stats.py: Contains functions to graph stats of games in the DB

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from database.db_manager import db_function as db

# TODO
# Connect to db and read the games

# TEMP: replace with real data once DB done
def completed_sessions():   
    all_sessions = db.get_all_map_and_id()
    completed = []

    for row in all_sessions:
        map_id = row[0]
        sessions = db.get_session_id_and_map(map_id)  

        for session in sessions:
            session_id = session[0]
            status = db.get_completion_status(session_id)
            time = db.get_completion_time(session_id)

            if status == 1:
                completed.append({
                    "map_id": map_id,
                    "session_id": session_id,
                    "time_spent": time,
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

