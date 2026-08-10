import matplotlib.pyplot as plt
import json
import plotter

def main():
    with open("89data.json","r") as file:
        data = json.load(file)

    total_msg = data["totalMsg"]
    timeToActiveView = data["timeToActiveView"]
    timeToTotalView = data["timeToTotalView"]

    plotter.plotFreq(total_msg)
    plotter.plotStuff([timeToActiveView,timeToTotalView],["timeToActiveView","timeToTotalView"])

main()