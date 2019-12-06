import win32gui
import win32con
import win32api
import time
import os, sys
import getopt
import subprocess
from PIL import ImageGrab, Image
from threading import Timer
from threading import Thread
import _thread

class ADB:
    def __init__(self,device_Name,screen_Size):
        #self.adb_Path = "C:/Program Files (x86)/Nox/bin/nox_adb.exe"  #夜神
        self.adb_Path = "C:/XuanZhi/LDPlayer/adb.exe"   #雷電
        self.screen_Size = screen_Size
        self.device_Name = device_Name
        self.Nox_Path = r"C:/Program Files (x86)/Nox/bin/"
        self.LD_Path = r'C:/XuanZhi/LDPlayer/'
        self.hwnd = 0
        self.screen_Hot = None

    def Start_Game(self, Game_Activity_Name, device_Name=None):
        if device_Name ==None:
            device_Name = self.device_Name
            #adb -s 127.0.0.1:62001 shell am start -n air.jp.co.cygames.worldflipper/.AppEntry
        self.adb_call(device_Name, ['shell', 'am', 'start', '-n', Game_Activity_Name])

    def Shut_Down_Game(self, Game_Activity_Name, device_Name=None):
        if device_Name ==None:
            device_Name = self.device_Name
        self.adb_call(device_Name, ['shell', 'am', 'force-stop', Game_Activity_Name])

    def Keep_Game_ScreenHot(self,Emu_Index,file_Name):
        th = Thread(self.Keep_Game_ScreenHot_fn,args=[Emu_Index,file_Name])
        th.start()

    def Keep_Game_ScreenHot_fn(self,Emu_Index,file_Name):
        self.hwrd = self.Get_Self_Hwnd(Emu_Index)
        while 1:
            self.window_capture(hwnd=self.hwnd,fileName=file_Name)
            time.sleep(1)

    def Get_Self_Hwnd(self,index_Num):
        #device_List = self.Nox_Call()   #夜神
        device_List = self.LD_Call()  #雷電
        for k, device_Data in enumerate(device_List):
            if k != index_Num:
                continue
            hwnd = device_Data[3]
            return hwnd

    def Game_ScreenHot_By_Adb(self, device_Name=None, save_path=None):
        if device_Name == None:
            device_Name=self.device_Name
        if save_path == None:
            print('wrong!請輸入保存圖片的路徑')
        else:
            self.adb_call(device_Name, ['shell', 'screencap', '-p', '/sdcard/screen.png'])
            time.sleep(1)
            self.adb_call(device_Name, ['pull', '/sdcard/screen.png', save_path])
    def Get_Rect_Img(self,x1,y1,x2,y2):
        pass

    def Nox_Call(self):
        file_Path = self.Nox_Path + "NoxConsole.exe"
        output = subprocess.Popen([file_Path,"list2"], shell = True, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)

        end = []
        for line in output.stdout.readlines():
            output = line.decode("BIG5")
            output = output.strip()
            if output != "":
                output = output.split(",")
                end.append(output)
        return end

    def LD_Call(self):
        file_Path = self.LD_Path + "LDConsole.exe"  
        output = subprocess.Popen([file_Path,"list2"], shell = True, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)

        end = []
        for line in output.stdout.readlines():
            output = line.decode("BIG5")
            output = output.strip()
            if output != "":
                output = output.split(",")
                end.append(output)
        return end

    def window_cpature(self,hwnd,fileName):
        game_Rect = win32gui.GetWindowRect(int(hwnd))
        src_Image = ImageGrab.grab(game_Rect)

        src_Image = src_Image.resize(self,screen_Size,Image.ANTIALIAS)
        src_Image.save(fileName)
        self.screen_Hot = src_Image
        #print(type(src_Image))

    def Touch(self,x,y,device_Name=None):
        if device_Name is None:
            device_Name = self.device_Name
        x = str(x)
        y = str(y)
        self.adb_call(device_Name,["shell","input","tap",x,y])
    
    def Press(self,keypoint,device_Name=None):
        if device_Name is None:
            device_Name = self.device_Name
        keypoint = str(keypoint)
        self.adb_call(device_Name,["shell","input","keyevent",keypoint])

    def Text_Input(self,text,device_Name=None):
        if device_Name is None:
            device_Name = self.device_Name
        self.adb_call(device_Name,["shell","input","text",text])

    def adb_call(self,adb_Path,device_List):
        command = [self.adb_Path,"-s",self.device_Name]
        for order in device_List:
            command.append(order)
        print(command)
        subprocess.Popen(command)

    def Drag(self,x1,y1,x2,y2,x3,y3,deley_Time=1):
        x1 = x1 * 19199 / self.screen_Size[0]
        y1 = y1 * 10799 / self.screen_Size[1]
        x2 = x2 * 19199 / self.screen_Size[0]
        y2 = y2 * 10799 / self.screen_Size[1]
        x3 = x3 * 19199 / self.screen_Size[0]
        y3 = y3 * 10799 / self.screen_Size[1]

        
if __name__ == '_main__':
    #obj = ADB(device_Name='127.0.0.1:62001',screen_Size=[720,1280])  #夜神
    obj = ADB(device_Name='emulator-5556',screen_Size=[540,960])
    hawd = obj.Get_Self_Hwnd(0)
    obj.Drag(467,1164,400,1164,370,1164)