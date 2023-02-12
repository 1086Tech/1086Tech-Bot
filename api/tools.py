from threading import Thread
import time
import json
import pathlib

__all__ = ("TaskManager", "Logger")

class TaskManager:
    __slots__ = ("Perform_QueuingTask", "Perform_RunningTask")
    def __init__(self) -> None:
        self.Perform_QueuingTask = []
        self.Perform_RunningTask = []
    
    def __call__(self):
        while True:
            for each in self.Perform_QueuingTask:
                if not isinstance(each, Thread):
                    self.Perform_QueuingTask.remove(each)
            for each in self.Perform_QueuingTask:
                self.Perform_RunningTask.append(each)
                self.Perform_QueuingTask.remove(each)
            for each in self.Perform_RunningTask:
                each.start()
            for each in self.Perform_RunningTask:
                each.join()
            self.Perform_RunningTask.clear()
    def AddTask(self, Task:Thread) -> bool:
        if isinstance(Task, Thread):
            self.Perform_QueuingTask.append(Task)
            return True
        else:
            return False

def Logger(Message:str):
    with open("Run.log", "a", encoding='utf-8') as f:
        f.write("{} Message".format(time.strftime("%H:%M:%S")))

def JsonAuto(Json:dict, Action:str) -> bool|dict:
    PATH = pathlib.Path(__file__).parent.parent / "Admin.json"
    if Action == "WRITE":
        try:
            with open(PATH, "w+", encoding="utf-8") as file:
                file.write(json.dumps(Json))
            return True
        except:
            return False
    elif Action == "READ":
        try:
            with open(PATH, "rt", encoding="utf-8") as file:
                return(json.loads(file.read()))
        except:
            return False
    else:
        return False