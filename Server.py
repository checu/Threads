import os
import time
import shutil
import threading
import queue


serverFolder= "C:\\Users\\A672724\\Desktop\\PWspółbieżne\\Server"
exitFlag = 0
queueLock = threading.Lock()
workQueue = queue.Queue(0)

# tworzenie dysków na sererze
def Server(disksNumber, serverFolder):

    for i in range(1, disksNumber+1):

        disk=serverFolder+"\\"+"Disk"+str(i)

        if not os.path.exists(disk):
            os.makedirs(disk)

        open(disk+"\\config.txt","w+").close() #ma być plik csv

# zliczanie ilosci plikow dla danego uzytkownika na serverze
def numberOfFilesforUser(userName):

    itemList=os.listdir(serverFolder)
    diskNum=len(itemList)
    filesNumber=0
    filesList=[]
    for i in itemList:

        diskPath=serverFolder+"\\"+i+"\\"+userName

        if os.path.exists(diskPath):
            filesNumber+=len(os.listdir(diskPath))
            filesList+=os.listdir(diskPath)
# Server(5,serverFolder)
    return filesNumber, filesList

def Upload(item):




# tworzenie wątków

class myThread(threading.Thread):
    def __init__(self, threadID, name, q):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.q = q

    def run(self):
            print("Starting " + self.name)
            itemProcessing(self.name, self.q)
            print("Exiting " + self.name)

def itemProcessing(threadName, q):
        while not exitFlag:
            queueLock.acquire()
            if not workQueue.empty():
                item = q.get()
                queueLock.release()
                print("%s processing %s" % (threadName, item))
            else:
                queueLock.release()
                print("kolejka pusta")
                return
            time.sleep(1)

def threadsCall():

    threadList = ["watek"+str(i) for i in range(1,int((workQueue.qsize()+1)/2))]
    threads = []
    threadID = 1
    exitFlag = 0

    # tworzenie watków
    for threadName in threadList:
        thread = myThread(threadID, threadName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

    # czekanie na pusta kolejke
    while not workQueue.empty():
        pass
    exitFlag = 1

    # czekanie na zakonczenie wszystkich watkow
    for t in threads:
        t.join()
    print("Exiting Main Thread")

# threadsCall()
# print(numberOfFilesforUser("Marianna"))