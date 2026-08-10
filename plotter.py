# setup stuff

import pytchat, yt_dlp, time
import matplotlib.pyplot as plt
import random
import json

VIDEO_ID = "ewPQ7qMLv3E"
VIDEO_URL = "https://www.youtube.com/watch?v=ewPQ7qMLv3E"

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