import matplotlib.pyplot as plt
import random

def plotStuff(datas,titles):
    colors = ["blue","orange","yellow","red"]
    lineStyles = ["-","--"]
    markers = ["o","s"]

    for i in range(len(datas)):
       data = datas[i]
       x=[int(point[0]) for point in data]
       y=[int(point[1]) for point in data]
       plt.plot(x,y,marker=random.choice(markers),linestyle=random.choice(lineStyles),color=random.choice(colors),label=titles[i])

    plt.xlabel("x-axis")
    plt.ylabel("y-axis")

    plt.grid(True)
    plt.legend()
    plt.show()

def plotFreq(freqDict):
    names = list(freqDict.keys())
    freq = []
    for f in freqDict.values():
       freq.append(len(f))

    bars = plt.bar(names,freq,color="skyblue",edgecolor="black")

    plt.xlabel("Names")
    plt.ylabel("Count")
   
    plt.xticks(rotation=45,ha="right")

    for bar in bars:
       plt.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.1,int(bar.get_height()),ha="center",va="bottom")

    plt.grid(axis="y",linestyle="--",alpha=0.7)
    plt.tight_layout()
    plt.show()