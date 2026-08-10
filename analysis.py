import json
import plotter
from pathlib import Path

def main():
    dir = Path(__file__).resolve().parent
    filePath = dir/"89data.json"

    with open(filePath,"r") as file:
        data = json.load(file)

    total_msg = data["totalMsg"]
    timeToActiveView = data["timeToActiveView"]
    timeToTotalView = data["timeToTotalView"]

    # plotter.plotFreq(total_msg)
    # plotter.plotStuff([timeToActiveView,timeToTotalView],["timeToActiveView","timeToTotalView"])

    target_cnt = {}
    target = "goon"

    for name,msgs in total_msg.items():
        for msg in msgs:
            if target in msg:
                target_cnt.setdefault(name,0)
                target_cnt[name]+=1

    plotter.plotFreq2(target_cnt)

main()