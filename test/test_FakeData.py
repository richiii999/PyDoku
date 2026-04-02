# FakeData
# Test if can even graph at all

from sys import path
path.append(".")

import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("fakedata.csv")

plt.scatter(data['ID'], data['Time'], c=data['Time']) # 'c' = color

plt.colorbar(label="Time")
plt.title("Time per Game")
plt.xlabel("Game ID")
plt.yticks([]) # Hide y-axis entirely since we have colorbar

plt.show()
