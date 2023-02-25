from pathlib import Path

from threading import Thread, Lock
import json, os
from .typings import TaskManagerExit

__all__ = ("TaskManager", "Logger")

DefaultJSON = {"Root": None, "Admin": [], "BotQQ": None,"NotAllowUser":[], "BadWords": [], "AcceptPort": 5120, "PostIP": "127.0.0.1:5700", "@Me": None, "AdminGroup": []}

class TaskManager:
    __slots__ = ("Perform_QueuingTask", "Perform_RunningTask", "Status", "TaskLimit")
    def __init__(self, TaskLimit:int) -> None:
        self.Perform_QueuingTask:list[Thread] = []
        self.Perform_RunningTask:list[Thread] = []
        self.TaskLimit = TaskLimit
        self.Status = True
    
    def run(self):
        while self.Status:
            try:
                if len(self.Perform_QueuingTask)+len(self.Perform_RunningTask) > 0:
                    for each in self.Perform_QueuingTask:
                        self.Perform_RunningTask = [t for t in self.Perform_RunningTask if t.is_alive()]
                        if not isinstance(each, Thread):
                            self.Perform_QueuingTask.remove(each)
                            continue
                        elif self.TaskLimit:
                            if len(self.Perform_RunningTask) >= self.TaskLimit:
                                continue
                        self.Perform_RunningTask.append(each)
                        self.Perform_QueuingTask.remove(each)
                        self.Perform_RunningTask[-1].start()
            except BaseException as e:
                break
        if self.Status:
            Error = TaskManagerExit("任务管理器异常退出")
            raise Error
    def AddTask(self, Task:Thread) -> bool:
        if isinstance(Task, Thread):
            self.Perform_QueuingTask.append(Task)
            return True
        else:
            return False

FileLock = Lock()

def JsonAuto(Json:dict, Action:str, PATH:Path) -> bool|dict:
    if not PATH.exists():
        with FileLock:
            with open(PATH, "w+", encoding="utf-8") as f:
                f.write(json.dumps(DefaultJSON))
    if Action == "WRITE":
        try:
            with FileLock:
                with open(PATH, "w+", encoding="utf-8") as file:
                    file.write(json.dumps(Json))
                return True
        except:
            return False
    elif Action == "READ":
        try:
            with FileLock:
                with open(PATH, "rt", encoding="utf-8") as file:
                    Res:dict = json.loads(file.read())
            if Res.keys() == DefaultJSON.keys():
                return Res
            else:
                raise Exception
        except:
            os.remove(PATH)
            return DefaultJSON
    else:
        return False

def BadWord(Message:str, BadWordList:list) -> bool:
    if len([each for each in BadWordList if each in Message]) > 0:
        return True
    else:
        return False

TempLock = Lock()

def CodeReview(PATH:Path, Code: str, Group_id: int) -> bool:
    import random
    Message = {}

    with TempLock:
        try:
            with open(PATH/"temp.py", "w+", encoding="utf-8") as f:
                f.write(Code)
            from temp import Tech
            random_numbers = ""
            for i in range(1, random.randint(5, 10)):
                random_numbers += f"{str(random.randint(1, 100))} "
            random_numbers += str(random.randint(1, 100))
            tech1 = Tech(Mode=1, Number=random_numbers)
            Message[f'模式1输出\n{str(tech1)}, 原值{random_numbers}'] = Group_id
            random_number = random.randint(1, 100)
            tech2 = Tech(Mode=2, Number=random_number)
            Message[f'模式2输出\n{str(tech2)} 原数{random_number}'] = Group_id
            os.remove(PATH/"temp.py")
        except BaseException as e:
            Message[f'审核不通过，错误：{e}'] = Group_id
        return Message