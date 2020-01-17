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
        self.ADB = ADB(device_Name='emulator-5554',screen_Size=(560,960))
        #self.ADB = ADB(device_Name='emulator-5556',screen_Size=(560,960))

    def Game_Start(self):
        logging.info('啟動遊戲({}),等待 5 秒'.format('air.jp.co.cygames.worldflipper/.AppEntry'))
        self.ADB.Start_Game(Game_Activity_Name='air.jp.co.cygames.worldflipper/.AppEntry')
        time.sleep(5)

    def Game_Stop(self):
        logging.info('關閉遊戲({}),等待 5 秒'.format('air.jp.co.cygames.worldflipper'))
        self.ADB.Shut_Down_Game(Game_Activity_Name='air.jp.co.cygames.worldflipper')
        time.sleep(5)

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
        self.ADB.Touch(391,693)  ## OK  12/14更新位置
        #self.ADB.Touch(395,635)  ## OK (red-button)   old
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
        time.sleep(1)
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
        time.sleep(1)
        self.ADB.Touch(351,641)  ##OK
        time.sleep(1.5)
        logging.info('進行十連抽')
        self.ADB.Touch(351,641)  ##十連抽
        time.sleep(1.5)
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
            #self.ADB.Touch(529,25
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
        if starNumber >=2:
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
        time.sleep(1.5)
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
        count = 0
        self.ADB.Image_Grab(mode=('get_'+mode))
        stat = self.ADB.Recognize_Img(mode=mode)
        while stat != True:
            if mode == 'delete-button' and count >60:
                logging.error('當機！關閉遊戲並等待 3 秒後重啟')
                self.ADB.Start_Game(Game_Activity_Name='air.jp.co.cygames.worldflipper/.AppEntry')
                time.sleep(3)
            #print('目前狀態: ', stat)
            count = count +1
            self.ADB.Image_Grab(mode=('get_'+mode))
            stat = self.ADB.Recognize_Img(mode=mode)
        #time.sleep(0.3)

    ########################################################################
    ###
    ###    自動開房
    ###
    ########################################################################
    def Selete_Boss(self,boss_Number=0):
        logging.info('判斷是否已到boss選單')
        print('開始判斷是否已到boss選單')
        self.Check_Stat(mode='87snake-button')
        time.sleep(1)
        logging.info('已進入boss選單主頁面，開始開房')
        print('已進入boss選單主頁面，開始開房')
        if boss_Number == 0:
            self.ADB.Touch(79,449) ##大蛇
        if boss_Number == 1:
            self.ADB.Touch(82,549) ##光上
        if boss_Number == 2:
            self.ADB.Touch(88,666) ##白虎
        if boss_Number == 3:
            self.ADB.Touch(82,763) ##暗上
        if boss_Number == 4:
            self.ADB.Touch(74,859) ##水上
        if boss_Number == 5:
            self.ADB.Swipe(273,845,273,214)
            time.sleep(0.4)
            self.ADB.Touch(273,586)##火上
        if boss_Number == 6:
            self.ADB.Swipe(273,845,273,214)
            time.sleep(0.4)
            self.ADB.Touch(273,703)##不死
        if boss_Number == 7:
            self.ADB.Swipe(273,845,273,214)
            time.sleep(0.4)
            self.ADB.Touch(273,808)##貓頭鷹
        time.sleep(1)
        self.ADB.Touch(269,351)
        time.sleep(1)
        self.ADB.Touch(278,713)
        time.sleep(1)
        pass

    def Check_DoudlePrice(self):
        pass

    def Check_MultiPlay(self):
        pass

    def Check_SecondMenber(self,party_Member=0):
        logging.info('判斷是否進入第二名成員')
        print('判斷是否進入第二名成員')
        self.ADB.Image_Grab(mode='get_roomstatSecondMenberStat-button')
        stat = self.ADB.Recognize_Img(mode='roomstatSecondMenberStat-button')
        while stat != False:
            roomStat = self.Is_Dismissed()
            if roomStat == True:
                logging.info('房間已被解散')
                print('房間已被解散')
                return 'dismissed'
            self.ADB.Image_Grab(mode='get_roomstatSecondMenberStat-button')
            stat = self.ADB.Recognize_Img(mode='roomstatSecondMenberStat-button')
        logging.info('已有第二名成員')
        print('已有第二名成員')
        if party_Member == 2:
            logging.info('已滿人，出發')
            print('已滿人，出發')
            time.sleep(1)
            self.ADB.Touch(398,629)
            time.sleep(1)
            return 'party is full!'
            pass
        time.sleep(1)
        return 'second member joined!'
        pass

    def Is_FullPayty(self):
        logging.info('判斷是否滿人')
        print('判斷是否滿人')
        self.ADB.Image_Grab(mode='get_roomstat-button')
        stat = self.ADB.Recognize_Img(mode='roomstat-button')
        while stat != False:
            roomStat = self.Is_Dismissed()
            if roomStat == True:
                logging.info('房間已被解散')
                print('房間已被解散')
                return 'dismissed'
            self.ADB.Image_Grab(mode='get_roomstat-button')
            stat = self.ADB.Recognize_Img(mode='roomstat-button')
        logging.info('已滿人，出發')
        print('已滿人，出發')
        time.sleep(1)
        self.ADB.Touch(398,629)
        time.sleep(1)
        return 'party is full!'
        pass

    def Is_RoomCreated(self,party_Member=0):
        logging.info('判斷是否已開啟房間')
        print('判斷是否已開啟房間')
        self.Check_Stat(mode='roomstat-button')
        logging.info('已建立房間')
        print('已建立房間')
        time.sleep(1)
        self.ADB.Touch(73,628)  ##按下準備
        time.sleep(0.6)
        self.ADB.Touch(270,708) ##按下招募
        time.sleep(0.6)
        self.ADB.Touch(256,402) ##按下招募好友
        if party_Member != 2:
            time.sleep(0.6)
            self.ADB.Touch(270,708) ##按下招募-第二次
            time.sleep(0.6)
            self.ADB.Touch(278,490) ##按下招募鈴鐺
        time.sleep(1)
        pass

    def Is_Dismissed(self):
        logging.info('判斷是否被解散房間')
        print('判斷是否被解散房間')
        self.ADB.Image_Grab(mode='get_dismissed-button')
        stat = self.ADB.Recognize_Img(mode='dismissed-button')
        return stat   ##ok button in 268,620
        pass

    def Check_In_Boss_Fight(self):
        logging.info('判斷是否已開始戰鬥')
        print('判斷是否已開始戰鬥')
        self.ADB.Image_Grab(mode='get_bossFightStat-button')
        stat = self.ADB.Recognize_Img(mode='bossFightStat-button')
        while stat != True:
            roomStat = self.Is_Dismissed()
            if roomStat == True:
                logging.info('房間已被解散')
                print('房間已被解散')
                return 'dismissed'
            self.ADB.Touch(398,629)
            self.ADB.Image_Grab(mode='get_bossFightStat-button')
            stat = self.ADB.Recognize_Img(mode='bossFightStat-button')
        logging.info('已開始戰鬥，執行退出戰鬥')
        print('已開始戰鬥，執行退出戰鬥')
        time.sleep(1)
        self.ADB.Touch(33,54)
        time.sleep(1)
        self.ADB.Touch(25,929)
        time.sleep(1)
        self.ADB.Touch(399,622)
        time.sleep(1)
        return 'go back to menu'
        pass






