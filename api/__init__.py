"""
CoolPlayLin-Bot的API基础
"""

from . import cqbotapi as NormalAPI
from . import util as ToolAPI
from . import typings

def Group_Msg(Server:NormalAPI.APIs, Group_id:int, User_id:int, Message:str, Message_Id:int, Dates:dict) -> bool:
    import random
    from requests import get
    from pathlib import Path

    if not isinstance(Server, NormalAPI.APIs):
        return False
    try:
        MessageList = {}
        Admin:bool = Group_id in Dates["AdminGroup"]

        if User_id in Dates['NotAllowUser']:
            MessageList[Group_id] = '管理员不允许你使用'
        elif ToolAPI.BadWord(Message, Dates['BadWords']):
                Server.Delete_Msg(message_id=Message_Id)
                MessageList[Group_id] = "检测到敏感内容, 已尝试撤回"
        else:
            if Dates["@Me"]+'冷静' in Message and Admin:
                if not User_id in Dates['Admin']:
                    MessageList[Group_id] = "你没有Admin权限"
                else:
                    User = int(Message.replace(Dates["@Me"]+"冷静", ""))
                    Server.Set_Group_Ban(Group_id, User, 60)
                    MessageList[Group_id] = "已尝试冷静此人"
            elif Dates["@Me"]+'禁言大转盘' in Message and Admin:
                if not User_id in Dates['Admin']:
                    MessageList[Group_id] = "你没有Admin权限"
                else:
                    User = int(Message.replace(Dates["@Me"]+"禁言大转盘", ""))
                    Min = random.randint(1, 60)
                    Server.Set_Group_Ban(Group_id, User, 60*Min)
                    MessageList[Group_id] = "恭喜获得{}分钟".format(Min)
            elif Dates["@Me"]+'关灯' in Message and Admin:
                Server.Set_Group_Whole_Ban(Group_id, True)
                MessageList[Group_id] = '全体禁言已启动'
            elif Dates["@Me"]+'开灯' in Message and Admin:
                Server.Set_Group_Whole_Ban(Group_id, False)
                MessageList[Group_id] = '全体禁言已停止'
            elif Dates["@Me"]+"代码审查" in Message:
                ToolAPI.CodeReview(Path(__file__).parent ,Message.replace(Dates["@Me"]+"代码审查", ""), Group_id)

            elif Message in [Dates["@Me"]+each for each in ["menu", "Menu", "MENU", "菜单","功能", "功能列表"]]:
                MessageList[Group_id] ="Hello，我是由CoolPlayLin开发并维护的开源QQ机器人，采用GPLv3许可证，项目直达 -> https://github.com/CoolPlayLin/CoolPlayLin-Bot\n我目前的功能\n1. 一言：获取一言文案"
            elif Dates["@Me"]+"Show AdminGroup" in Message:
                MessageList[Group_id] = '当前所管理的群\n{}'.format(Dates['AdminGroup'])
            elif Dates["@Me"]+"Add AdminGroup" in Message:
                if User_id in Dates['Admin']:
                    Group = int(Message.replace(Dates["@Me"]+"Add AdminGroup ", ""))
                    Dates['AdminGroup'].append(Group)
                    MessageList[Group_id] = '保存成功\n{}'.format(Dates['AdminGroup'])
                else:
                    MessageList[Group_id] = "你没有Admin权限"
            elif Dates["@Me"]+"Add This AdminGroup" in Message:
                if User_id in Dates['Admin']:
                    Dates['AdminGroup'].append(Group_id)
                    MessageList[Group_id] = '保存成功\n{}'.format(Dates['AdminGroup'])
                else:
                    MessageList[Group_id] = "你没有Admin权限"
            elif Dates["@Me"]+"Del AdminGroup" in Message:
                if User_id in Dates['Admin']:
                    Group = int(Message.replace(Dates["@Me"]+"Del AdminGroup ", ""))
                    if Group in Dates['AdminGroup']:
                        Dates['AdminGroup'].remove(Group)
                        MessageList[Group_id] = '保存成功\n{}'.format(Dates['AdminGroup'])
                    else:
                        MessageList[Group_id] = '不包含此项'
                else:
                    MessageList[Group_id] = "你没有Admin权限"
            elif Dates["@Me"]+"Refuse" in Message:
                if not User_id in Dates['Admin']:
                    MessageList[Group_id] = "你没有Admin权限"
                else:
                    User = int(Message.replace(Dates["@Me"]+"Refuse ", ""))
                    if User != Dates['Root']:
                        Dates['NotAllowUser'].append(User)
                        MessageList[Group_id] = '已将此用户添加到拒绝列表\n{}'.format(Dates['NotAllowUser'])
                    else:
                        MessageList[Group_id] = '不允许将Root用户添加到拒绝列表'
            elif Dates["@Me"]+"Accept" in Message:
                if not User_id in Dates['Admin']:
                    MessageList[Group_id] = "你没有管理权限"
                else:
                    User = int(Message.replace(Dates["@Me"]+"Accept ", ""))
                    if User in Dates['NotAllowUser']:
                        Dates['NotAllowUser'].remove(User)
                        MessageList[Group_id] = '已将此用户从拒绝列表移除\n{}'.format(Dates['NotAllowUser'])
                    else:
                        MessageList[Group_id] = '此用户不在拒绝列表中'
            elif Dates["@Me"]+"RefuseList" in Message:
                MessageList[Group_id] = '拒绝用户列表\n{}'.format(Dates['NotAllowUser'])
            elif Dates["@Me"]+"Set Root" in Message:
                if Dates['Root'] == None:
                    Dates['Root'] = User_id
                    Dates['Admin'].append(User_id)
                    MessageList[Group_id] = 'Root成功设置为{}'.format(str(User_id))
                else:
                    MessageList[Group_id] = 'Root用户已设置，请勿重复设置'
            elif Dates["@Me"]+"Show Admin" in Message:
                if User_id != Dates['Root']:
                    MessageList[Group_id] = "你没有Root权限"
                else:
                    MessageList[Group_id] = "当前管理员列表\n{}".format(str(Dates['Admin']))
            elif Dates["@Me"]+'Add Admin' in Message:
                if User_id != Dates['Root']:
                    MessageList[Group_id] = "你没有Root权限"
                else:
                    Dates['Admin'].append(int(Message.replace(Dates["@Me"]+"Add Admin ", "")))
                    MessageList[Group_id] = "保存成功\n{}".format(str(Dates['Admin']))
            elif Dates["@Me"]+'Del Admin' in Message:
                if User_id != Dates['Root']:
                    MessageList[Group_id] = "你没有Root权限"
                else:
                    _ = int(Message.replace(Dates["@Me"]+"Del Admin ", ""))
                    if _ in Dates['Admin']:
                        Dates['Admin'].remove(_)
                        MessageList[Group_id] = "保存成功\n{}".format(str(Dates['Admin']))
                    else:
                        MessageList[Group_id] = "此用户不在Admin中"
            elif Dates["@Me"]+'Status' in Message:
                MessageList[Group_id] = "功能未实现"
            elif Message in [Dates["@Me"]+'获取一言', Dates["@Me"]+'一言', Dates["@Me"]+'文案']:
                MessageList[Group_id] = (get("https://v1.hitokoto.cn/").json()['hitokoto'])
            elif Dates["@Me"].replace(" ", "") in Message:
                MessageList[Group_id] = "干啥子"
        # 集中发送消息
        Groups = MessageList.keys()
        for each in Groups:
            Server.Send_Group_Msg(Groups, MessageList[each])

        return True
    except BaseException as e:
        MessageList[Group_id] = "错误：\n{}".format(e)
        raise

def AutoSave(Task:ToolAPI.TaskManager, Server:NormalAPI.APIs, Dates:dict, PATH) -> None:
    from threading import Thread

    if Dates != ToolAPI.JsonAuto(None, "READ", PATH):
        ToolAPI.JsonAuto(Dates, "WRITE", PATH)
    if Dates["BotQQ"] is None:
        try:
            QQ = Server.Get_Login_Info().json()['data']['user_id']
            Dates["BotQQ"] = QQ
            Dates["@Me"] = "[CQ:at,qq={}] ".format(QQ)
            return True
        except:
            return False