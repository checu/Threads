import os
import time
import shutil
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import queue
import Server

localFolder= "C:\\Users\\A672724\\Desktop\\PWspółbieżne\\Clients"

def Client(username,localFolder):

    #ustawianie kolejki
    userQueue=[]


    clientFolder = localFolder+"\\"+username

    if not os.path.exists(clientFolder):
        os.makedirs(clientFolder)

    filesNumber=len(os.listdir(clientFolder))



# upload to server load from server

    def UploadOrLoad():

        filesNumberS = Server.numberOfFilesforUser(username)[0]


        if filesNumber > filesNumberS:
            #             send to server
            itemsSet=set(os.listdir(clientFolder))-set(Server.numberOfFilesforUser(username)[1])
            userQueue=list(itemsSet)
            appendQueue(userQueue)
            print("send")
        elif filesNumber < filesNumberS:
            #             load form server
            itemsSet = set(set(Server.numberOfFilesforUser(username)[1]-os.listdir(clientFolder)))
            userQueue = list(itemsSet)
            appendQueue(userQueue)
            print("load")


    # UploadOrLoad()
    print(os.listdir(clientFolder))
    print(Server.numberOfFilesforUser(username)[1])

    UploadOrLoad()

#dodawanie plikow do kolejki
def appendQueue(itemsQueue):

    Server.queueLock.acquire()
    for file in itemsQueue:
        Server.workQueue.put(file)
    Server.queueLock.release()
    print(Server.workQueue)

 #     klasa do sprawdzania updatu pliku w folderze lokalnym uzytkownika

    def realTimeObservation():
        class Watcher():

            def __init__(self):
                self.observer=Observer()

            def run(self):
                event_handler=Handler()
                self.observer.schedule(event_handler,clientFolder,recursive=True)
                self.observer.start()
                try:
                    time.sleep(15)
                except:
                    self.observer.stop()
                    print("Error")

                self.observer.join()

        class Handler(FileSystemEventHandler):

            def on_any_event(self, event):

                if event.is_directory:
                    return None

                elif event.event_type=='created':
                    print("File created", event.src_path)

                elif event.event_type=='modified':
                    shutil.copy(event.src_path,"C:\\Users\\A672724\\Desktop\\PWspółbieżne\\Server\\Disk1")
                    print("File modified",event.src_path)

        if __name__=='__main__':
            w=Watcher()
            w.run()


Client("Marianna",localFolder)
Server.threadsCall()
