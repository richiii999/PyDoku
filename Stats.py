
# Stats.py: Contains functions to graph stats of games in the DB

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# TODO
# Connect to db and read the games

# TEMP: replace with real data once DB done
data = pd.read_csv("fakedata.csv")

def GamesByTime():
    """Graphs games by ID / Time (Chronological play order)"""
    sns.scatterplot(x="ID", y="Time", data=data, hue="Time")

    plt.title("Time per game")
    # x/y label already set from DB
    plt.show()
