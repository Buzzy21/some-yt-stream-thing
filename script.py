# setup stuff

import pytchat, yt_dlp, time
import matplotlib.pyplot as plt
import random
import json
import threading

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

completeTotalViewcount = []

chatInfo = []
timeToActiveView = []
timeToTotalView = []

dataLock = threading.Lock()

def dumper(timeDump, sleepTime):
    lastTime = time.time()

    while chat.is_alive():
        currTime = time.time()
        if lastTime+timeDump<currTime:
            saveStorage()
            lastTime = currTime
            currTime = time.time()

        time.sleep(sleepTime)

    saveStorage()
   
def constantViewCounter(sleepTime):
    while chat.is_alive():
        viewCount = getTotalViewCount()
        currTime = time.time()

        with dataLock:
            completeTotalViewcount.append([currTime,viewCount])
        time.sleep(sleepTime)

   
def periodicCounter(sleepTime, epsilon):
    lastTime = time.time()

    while chat.is_alive():
        currTime = time.time()
        # past msg record reset/analysis
        # print(f"{lastTime} : {currTime}")

        for c in chat.get().sync_items():
            names = c.author.name
            msgs = c.message

            with dataLock:
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
               
            with dataLock:
                uniqueNames = set()
                for c in chatInfo:
                    uniqueNames.add(c[0])

                activeCount = len(uniqueNames)
                # print(f"Active count: {activeCount}")
                timeToActiveView.append([currTime,activeCount])
                timeToTotalView.append([currTime,viewCount])
                chatInfo.clear()

            # reset
            lastTime = currTime
        time.sleep(sleepTime)


    saveStorage()

def saveStorage():
    with dataLock:
        toStore = {"totalMsg":  totalMsg, "timeToActiveView":timeToActiveView,"timeToTotalView":timeToTotalView,"completeTotalViewcount":completeTotalViewcount}
        with open("storage.json","w") as file:
            json.dump(toStore,file,indent=4)
        print(f"Dumped at {time.time()}")


def main():
    threadConstant = threading.Thread(target=constantViewCounter,args=(0.1,))
    threadPeriodic = threading.Thread(target=periodicCounter,args=(1,100))
    threadDump = threading.Thread(target=dumper,args=(600,1))

    threadConstant.start()
    threadPeriodic.start()
    threadDump.start()

    threadConstant.join()
    threadPeriodic.join()
    threadDump.join()

    print("yay we done")
   
main()