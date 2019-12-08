#from GitHub.worldFlipper_ATS.adb import ADB
from adb import ADB
import time, datetime
import os
import logging



class controller:
    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    DATE_FORMAT = '%Y%m%d %H:%M:%S'
    DATE_TODAY = '{}{}{}'.format(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)
    LOG_FILE = './logs/Logs_{}.log'.format(DATE_TODAY)
    if not os.path.exists(LOG_FILE):
        files = open(LOG_FILE,"w+")
        files.close()
    logging.basicConfig(level=logging.INFO, filename=LOG_FILE, format=LOGGING_FORMAT, datefmt=DATE_FORMAT)
    def __init__(self):
        #self.ADB = ADB(device_Name='127.0.0.1:62001',screen_Size=(720,1280))  #夜神
        self.ADB = ADB(device_Name='emulator-5556',screen_Size=(560,960))

    def Game_Start(self):
        logging.info('啟動遊戲({}),等待 5 秒'.format('air.jp.co.cygames.worldflipper/.AppEntry'))
        self.ADB.Start_Game(Game_Activity_Name='air.jp.co.cygames.worldflipper/.AppEntry')
        time.sleep(5)

    def Game_Stop(self):
        logging.info('關閉遊戲({}),等待 2 秒'.format('air.jp.co.cygames.worldflipper'))
        self.ADB.Shut_Down_Game(Game_Activity_Name='air.jp.co.cygames.worldflipper')
        time.sleep(2)

    def Delete_Record(self):
        logging.info('為了刪除紀錄，開始判斷是否進入遊戲主頁面')
        print('為了刪除紀錄，開始判斷是否進入遊戲主頁面(透過右上角button)')
        self.Check_Stat(mode='delete-button')
        logging.info('已進入遊戲主頁面，開始刪除紀錄')
        print('開始刪除紀錄')
        self.ADB.Touch(500,56)  ##右上角選單
        time.sleep(2)
        self.ADB.Touch(392,482)  ##清除紀錄選項(垃圾桶)
        time.sleep(2)
        self.ADB.Touch(395,635)  ## OK (red-button)
        time.sleep(1)
        self.ADB.Touch(395,635)  ## OK_double-check (red-button)
        time.sleep(8)
        ##通信中,等待遊戲重啟
        #function 判斷是否到遊戲啟動首頁
        ## goto login_game

    def Login_Game(self,achiveTime='firstTime'):
        logging.info('開始判斷是否進入遊戲主頁面')
        print('開始判斷是否進入遊戲主頁面(透過右上角button)')
        self.Check_Stat(mode='delete-button')
        logging.info('已進入遊戲主頁面，點擊螢幕進入遊戲')
        print('已進入遊戲主頁面，點擊螢幕進入遊戲')
        self.ADB.Touch(395,635) ##點擊螢幕
        if achiveTime == 'firstTime':
            logging.info('新帳號第一次進入遊戲，開始判斷是否出現同意')
            print('新帳號第一次進入遊戲，開始判斷是否出現同意')
            self.Check_Stat(mode='agree-button')
            logging.info('已出現，點擊同意')
            print('已出現，點擊同意')
            self.ADB.Touch(395,635)  ##同意
            logging.info('開始判斷是否是否出現新手教學')
            print('開始判斷是否是否出現新手教學')
            self.Check_Stat(mode='canceltutorial-button')
            logging.info('已出現，點擊取消')
            print('已出現，點擊取消')
            self.ADB.Touch(151,623)  ##取消 (red-button)
            time.sleep(2)
            self.ADB.Touch(151,623)  ##取消 again(red-button)
            time.sleep(2)
            self.ADB.Touch(273,803)  ##ok again(red-button)
            time.sleep(2)
            for i in range(5):
                self.ADB.Touch(385,901)  ##下一步x5
                time.sleep(0.8)
            logging.info('開始判斷是否是否出現取名ok')
            print('開始判斷是否是否出現取名ok')
            self.Check_Stat(mode='nameconfirm-button')  ##判斷是否出現取名ok
            logging.info('已出現，確認取名')
            print('已出現，確認取名')
            self.ADB.Touch(269,465) ##ok (green-button)
            time.sleep(1.5)
            self.ADB.Touch(395,635)  ## OK (red-button)
        ##通信中
        ##function 判斷是否出現抽卡區
        time.sleep(2)
        ## goto summoning
    
    def Summoning(self):
        logging.info('開始判斷是否是否找到抽卡區')
        print('開始判斷是否是否找到抽卡區')  #這邊太慢
        self.ADB.Image_Grab(mode='get_summon-button')
        stat = self.ADB.Recognize_Img(mode='summon-button')
        while stat != True:
            self.ADB.Image_Grab(mode='get_summon-button')
            stat = self.ADB.Recognize_Img(mode='summon-button')
        logging.info('已看到抽卡區，點擊進入抽卡區')
        print('已看到抽卡區，點擊進入抽卡區')
        self.ADB.Touch(407,933)  ##進入抽卡區
        time.sleep(1.5)
        self.ADB.Touch(233,663)  ##進行強制單抽  (保底四星,有機會出五星)
        time.sleep(1.5)
        self.ADB.Touch(395,635)  ## OK (red-button)
        logging.info('開始判斷是否找到skip按鈕')
        print('開始判斷是否找到skip按鈕')
        self.Check_Stat(mode='skip-button')
        logging.info('已找到，按下skip')
        print('已找到，按下skip')
        self.ADB.Touch(529,25)  #skip
        logging.info('開始判斷是否是否抽完了')
        print('開始判斷是否是否抽完了')
        self.ADB.Image_Grab(mode='get_got4starconfirm-button')
        stat = self.ADB.Recognize_Img(mode='got4starconfirm-button')
        while stat != True:
            self.ADB.Touch(529,25)
            self.ADB.Image_Grab(mode='get_got4starconfirm-button')
            stat = self.ADB.Recognize_Img(mode='got4starconfirm-button')
        logging.info('已抽完，按下OK確認')
        print('已抽完，按下OK確認')
        time.sleep(1)
        self.ADB.Touch(272,620)  ##OK  
        time.sleep(1)
        self.ADB.Touch(476,833)  ##回上一頁
        ##讀取中
        logging.info('開始判斷是否是否出現送禮')
        print('開始判斷是否是否出現送禮')
        self.ADB.Image_Grab(mode='get_gotpriceconfirm-button')
        stat = self.ADB.Recognize_Img(mode='gotpriceconfirm-button')
        while stat != True:  #判斷是否出現送禮
            self.ADB.Touch(529,25)  #連點
            self.ADB.Image_Grab(mode='get_gotpriceconfirm-button')
            stat = self.ADB.Recognize_Img(mode='gotpriceconfirm-button')
        logging.info('已收到送禮，按下接收')
        print('已收到送禮，按下接收')
        self.ADB.Touch(351,641)  ##接收禮物按鈕
        logging.info('開始判斷是否是否出現ok')
        print('開始判斷是否是否出現ok')
        self.ADB.Image_Grab(mode='get_afterpriceconfirmok-button')
        stat = self.ADB.Recognize_Img(mode='afterpriceconfirmok-button')
        while stat != True:  ##判斷是否出現ok
            self.ADB.Touch(529,25)  #連點
            self.ADB.Image_Grab(mode='get_afterpriceconfirmok-button')
            stat = self.ADB.Recognize_Img(mode='afterpriceconfirmok-button')
        logging.info('已出現，按下OK確認')
        print('已出現，按下OK確認')
        self.ADB.Touch(351,641)  ##OK
        time.sleep(1)
        logging.info('進行十連抽')
        self.ADB.Touch(351,641)  ##十連抽
        time.sleep(1)
        self.ADB.Touch(351,641)  ##十連抽-確定
        logging.info('開始判斷是否找到skip按鈕')
        print('開始判斷是否找到skip按鈕')
        self.Check_Stat(mode='skip-button')
        logging.info('已找到，按下skip')
        print('已找到，按下skip')
        self.ADB.Touch(529,25)  #skip
        time.sleep(1)
        ## force-stop Game
    
    def Check_Box(self):
        logging.info('判斷是否出現包包選項')
        print('開始判斷是否出現包包選項')
        self.ADB.Image_Grab(mode='get_member-button')
        stat = self.ADB.Recognize_Img(mode='member-button')
        while stat != True:  ##function 判斷是否出現包包
            self.ADB.Touch(529,25)
            self.ADB.Touch(229,928)
            self.ADB.Image_Grab(mode='get_member-button')
            stat = self.ADB.Recognize_Img(mode='member-button')
        logging.info('已出現，打開包包')
        print('已出現，打開包包')
        time.sleep(1)
        self.ADB.Touch(495,105)  ##打開包包
        time.sleep(4)
        ## goto star Analysis

    def Star_Analysis(self):
        logging.info('擷取包包內照片')
        print('開始擷取包包內照片')
        self.ADB.Image_Grab(mode='get_star')
        logging.info('判斷角色星數')
        print('開始判斷角色星數')
        starNumber = self.ADB.Recognize_Img(mode='star')
        self.ADB.Touch(35,921)  ##離開角色包包
        if starNumber >=1:
            logging.info('得到結果,獲得五星角色 {} 隻,開始截圖保存至指定目錄'.format(starNumber))
            print('得到結果,獲得五星角色 {} 隻,開始截圖保存至指定目錄'.format(starNumber))
            self.ADB.Game_ScreenHot_By_Adb(save_path='./image/account/waitForAnalysis.jpg')
        return starNumber

    def Get_Account_ID(self):
        logging.info('判斷是否已回到首頁')
        print('開始判斷是否已回到首頁')
        self.ADB.Image_Grab(mode='get_summon-button')
        stat = self.ADB.Recognize_Img(mode='summon-button')
        while stat != True:
            self.ADB.Touch(35,921)  ##上一頁
            self.ADB.Image_Grab(mode='get_summon-button')
            stat = self.ADB.Recognize_Img(mode='summon-button')
        logging.info('已回到首頁，進入\'其他\'選單')
        print('已回到首頁，進入\'其他\'選單')
        self.ADB.Touch(492,921)  #進入'其他'選單
        time.sleep(1)
        self.ADB.Touch(267,851)  #點擊引繼
        logging.info('判斷是否已進到準備引繼的選單')
        print('開始判斷是否已進到準備引繼的選單')
        self.ADB.Image_Grab(mode='get_setaccount-button')
        stat = self.ADB.Recognize_Img(mode='setaccount-button')
        while stat != True:
            self.ADB.Image_Grab(mode='get_setaccount-button')
            stat = self.ADB.Recognize_Img(mode='setaccount-button')
        logging.info('已進入，開始引繼')
        print('已進入，開始引繼')
        time.sleep(0.5)
        self.ADB.Touch(265,583)  #點擊開始引繼
        time.sleep(1)
        self.ADB.Touch(388,816)  #ok
        time.sleep(1)
        self.ADB.Touch(266,490)  #點擊使用引繼碼
        time.sleep(1)
        self.ADB.Touch(270,659)  #ok
        time.sleep(1)
        self.ADB.Touch(263,566)  #點擊生成引繼碼
        time.sleep(1)
        self.ADB.Touch(261,354)  #點擊密碼框
        time.sleep(0.5)
        self.ADB.Text_Input('4700worldFlipper')
        time.sleep(0.5)
        self.ADB.Touch(261,413)  #點擊確認密碼框
        time.sleep(0.5)
        self.ADB.Text_Input('4700worldFlipper')
        time.sleep(0.5)
        self.ADB.Touch(70,597)  #勾選同意條款
        time.sleep(0.5)
        self.ADB.Touch(268,700)  #下一步
        time.sleep(1)
        #通信中

    def Recognize_Account(self,starNumber=0):
        logging.info('判斷是否已引繼成功得到引繼碼')
        print('開始判斷是否已引繼成功得到引繼碼')
        self.ADB.Image_Grab(mode='get_accountconfirm-button')
        stat = self.ADB.Recognize_Img(mode='accountconfirm-button')
        while stat != True:
            self.ADB.Image_Grab(mode='get_accountconfirm-button')
            stat = self.ADB.Recognize_Img(mode='accountconfirm-button')
        account = self.ADB.Image_Grab(mode='get_account')
        logging.info('成功獲得。將獲得的引繼碼({})存入指定目錄'.format(account))
        print('開始將獲得的引繼碼({})存入指定目錄'.format(account))
        os.rename('./image/account/waitForAnalysis.jpg','./image/account/{}_fiveStar/{}.jpg'.format(starNumber,account))

    def Check_Stat(self,mode=None):
        time.sleep(3)
        self.ADB.Image_Grab(mode=('get_'+mode))
        stat = self.ADB.Recognize_Img(mode=mode)
        while stat != True:
            #print('目前狀態: ', stat)
            self.ADB.Image_Grab(mode=('get_'+mode))
            stat = self.ADB.Recognize_Img(mode=mode)
        #time.sleep(0.3)

    
        




