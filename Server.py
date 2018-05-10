import os
import time
import shutil
import threading

serverFolder= "C:\\Users\\A672724\\Desktop\\PWspółbieżne\\Server"

def Server(diskNumber, serverFolder):

    for i in range(1, diskNumber+1):

        disk=serverFolder+"\\"+"Disk"+str(i)

        if not os.path.exists(disk):
            os.makedirs(disk)

        open(disk+"\\config.txt","w+").close()



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
    return filesNumber,filesList

# print(numberOfFilesforUser("Marianna"))