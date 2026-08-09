# setup stuff

import pytchat, yt_dlp, time
import matplotlib.pyplot as plt
import random
import json

VIDEO_ID = ""
VIDEO_URL = ""

ydl_opts = {'quiet': True, 'simulate': True}
chat = pytchat.create(video_id=VIDEO_ID)

def getConcurrentViewCount():
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(VIDEO_URL, download=False)

    return  info.get("concurrent_viewcount")

def getTotalViewCount():
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(VIDEO_URL, download=False)

    return  info.get("view_count")

def askViewCount(): # last resort
    return input("Enter viewcount: ")

totalMsg = {}


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
   
def main():
    lastTime = time.time()
    currTime = time.time()
    iterations = 0
    iterationNeed = 1
    epsilon = 600

    chatInfo = []

    timeToActiveView = []
    timeToTotalView = []

    while chat.is_alive():
        # past msg record reset/analysis
        # print(f"{lastTime} : {currTime}")

        for c in chat.get().sync_items():
            names = c.author.name
            msgs = c.message
            chatInfo.append([names,msgs])

            totalMsg.setdefault(names,[]).append(msgs)

        """
        if lastTime + epsilon < currTime:
           plotFreq(totalMsg)
           lastTime=currTime
           """

        if lastTime + epsilon < currTime: 
            print(f"Iteration at: {currTime}")
            viewCount = getConcurrentViewCount()
            if viewCount==None:
               print("No concurrent") 
               viewCount = getTotalViewCount()

            # viewCount = askViewCount()
               
            uniqueNames = set()
            for c in chatInfo:
               uniqueNames.add(c[0])

            activeCount = len(uniqueNames)
            # print(f"Active count: {activeCount}")
            timeToActiveView.append([currTime,activeCount])
            timeToTotalView.append([currTime,viewCount])

            iterations += 1

            if(iterations % 2 == 0):
            #    print(timeToActiveView)
            #    plotStuff([timeToActiveView,timeToTotalView],["active views","total views"])
            
                # store stuff
                toStore = {"totalMsg":  totalMsg, "timeToActiveView":timeToActiveView,"timeToTotalView":timeToTotalView}
                with open("storage.json","w") as file:
                    json.dump(toStore,file,indent=4)
                print(f"Dumped at {currTime}")


            # reset
            lastTime = currTime
            chatInfo.clear()
        currTime = time.time()
        time.sleep(0.5)


    # store stuff and yes i used this twice and should prob make it a method but idk how lambda work in python
    toStore = {"totalMsg":  totalMsg, "timeToActiveView":timeToActiveView,"timeToTotalView":timeToTotalView}
    with open("storage.json","w") as file:
        json.dump(toStore,file,indent=4)
    print(f"Dumped at {currTime}")


main()
