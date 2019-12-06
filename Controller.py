#from GitHub.worldFlipper_ATS.adb import ADB
from adb import ADB
import time


class controller:
    def __init__(self):
        #self.ADB = ADB(device_Name='127.0.0.1:62001',screen_Size=(720,1280))  #夜神
        self.ADB = ADB(device_Name='emulator-5556',screen_Size=(560,960))

    def Game_Start(self):
        self.ADB.Start_Game(Game_Activity_Name='air.jp.co.cygames.worldflipper/.AppEntry')

    def Delete_Record(self):
        self.ADB.Touch(500,56)  ##右上角選單
        time.sleep(2.5)
        #function 判斷是否到遊戲啟動首頁
        self.ADB.Touch(392,482)  ##清除紀錄選項(垃圾桶)
        time.sleep(2.5)
        self.ADB.Touch(395,635)  ## OK (red-button)
        time.sleep(2.5)
        self.ADB.Touch(395,635)  ## OK_double-check (red-button)
        ##通信中,等待遊戲重啟
        #function 判斷是否到遊戲啟動首頁
        ## goto login_game

    def Login_Game(self,):
        self.ADB.Touch(395,635) ##點擊螢幕
        ##function 判斷是否出現同意
        self.ADB.Touch(395,635)  ##同意
        ##function 判斷是否出現新手教學
        self.ADB.Touch(151,623)  ##取消 (red-button)
        time.sleep(2)
        self.ADB.Touch(151,623)  ##取消 again(red-button)
        time.sleep(2)
        self.ADB.Touch(273,803)  ##ok again(red-button)
        time.sleep(2)
        for i in range(5):
            self.ADB.Touch(273,803)  ##下一步x5
            time.sleep(1.3)
        ##function 判斷是否出現取名ok
        self.ADB.Touch(269,465) ##ok (green-button)
        time.sleep(1.5)
        self.ADB.Touch(395,635)  ## OK (red-button)
        ##通信中
        ##function 判斷是否出現抽卡區
        time.sleep(2)
        ## goto summoning
    
    def Summoning(self):
        self.ADB.Touch(407,933)  ##進入抽卡區
        time.sleep(2)
        self.ADB.Touch(233,663)  ##進行強制單抽  (保底四星,有機會出五星)
        time.sleep(2)
        self.ADB.Touch(395,635)  ## OK (red-button)
        ##function 判斷是否出現skip
        self.ADB.Touch(529,25)  #skip
        while True:
            self.ADB.Touch(529,25)  #連點
            time.sleep(1.3)
            ##function 判斷是否出現ok
            ##if ok >> break
        time.sleep(1)
        self.ADB.Touch(272,620)  ##OK  
        time.sleep(1.5)
        self.ADB.Touch(476,833)  ##回上一頁
        ##讀取中
        ##function 判斷是否出現領取石頭+角色
        self.ADB.Touch(351,641)  ##領收
        while True:
            self.ADB.Touch(529,25)  #連點
            time.sleep(1.3)
            ##function 判斷是否出現ok
            ##if ok >> break
        time.sleep(1)
        self.ADB.Touch(351,641)  ##OK
        time.sleep(1.5)
        self.ADB.Touch(351,641)  ##十連抽
        time.sleep(1.5)
        self.ADB.Touch(351,641)  ##十連抽-確定
        ##function 判斷是否出現skip
        self.ADB.Touch(529,25)  #skip

    def 
        




