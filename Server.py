import os
import time
import shutil
import threading
import queue
from random import randint


serverFolder = "C:\\Users\\A672724\\Desktop\\PWspółbieżne\\Server"
disks={}
exitFlag = 0
# queueLock = threading.Lock()
# workQueue = queue.Queue(0)
FlagLoad=False

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
    pathList=[]
    for i in itemList:

        diskPath=serverFolder+"\\"+i+"\\"+userName

        if os.path.exists(diskPath):
            filesNumber+=len(os.listdir(diskPath))
            filesList+=os.listdir(diskPath)

            for file in os.listdir(diskPath):
                pathList.append(diskPath+"\\"+file)

    return filesNumber, filesList, pathList


# kontoler zapewnia rownomierne rozmieszczenie plikow w dyskach
def Controler():
    if not disks:
        disckList=os.listdir(serverFolder)
        values=[0]*len(disckList)

        for d in range(len(disckList)):
            disks[disckList[d]] = values[d]

        dysk=min(disks, key=disks.get)
        disks[dysk]+=1

    else:
        dysk=dysk=min(disks, key=disks.get)
        disks[dysk] += 1

    return dysk

def UpdateLogg(disk,item,type,user):

    # logg message
    curTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    conf = open(serverFolder + "\\" + disk + "\\config.txt", "a")
    conf.write(str(curTime + "      "+user+"      "+type+"      " + item + '\n'))
    conf.close()

def Upload(item,user):

    disk = Controler()

    source = "C:\\Users\\A672724\\Desktop\\PWspółbieżne\\Clients\\"+user+"\\" + item
    dest = serverFolder + "\\" + disk + "\\"+user

    if not os.path.exists(dest):
        os.mkdir(dest)

    shutil.copy(source, dest)

    UpdateLogg(disk,item,"Upload",user)


def Load(item,user):

    fileList=numberOfFilesforUser(user)[2]

    for file in fileList:
        doc= file.rpartition('\\')[-1]
        if item == doc:
            disk= file[44:50]
            source = file
            dest = "C:\\Users\\A672724\\Desktop\\PWspółbieżne\\Clients""\\"+user

            if not os.path.exists(dest):
                os.mkdir(dest)

            shutil.copy(source, dest)

            UpdateLogg(disk, item, "Load", user)


# tworzenie wątków

class myThread(threading.Thread):
    def __init__(self, threadID, name, q,user):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.q = q
            self.user = user

    def run(self):
            print("Starting " + self.name)
            itemProcessing(self.name, self.q,self.user)
            print("Exiting " + self.name)

def itemProcessing(threadName, q, userName):
        while not exitFlag:
            # queueLock.acquire()
            if not q.empty():
                item = q.get()
                time.sleep(randint(1, 15))
                if FlagLoad:
                    Load(item,userName)
                else:
                    Upload(item, userName)
                print("%s processing %s" % (threadName, item))
                # queueLock.release()
            else:
                # queueLock.release()
                print("kolejka pusta")
                return
            time.sleep(1)

def threadsCall(userName,workQueue):

    if(workQueue.qsize()>1):
        threadList = ["watek"+str(i) for i in range(1,int((workQueue.qsize()+2)/2))]
    else:
        threadList = ["watek1"]

    threads = []
    threadID = 1
    exitFlag = 0

    # tworzenie watków
    for threadName in threadList:
        thread = myThread(threadID, threadName, workQueue,userName)
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
# Controler()