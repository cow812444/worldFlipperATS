import win32gui
import win32con
import win32api
import time
import os, sys
import re
import getopt
import math
import subprocess
from PIL import ImageGrab, Image
from threading import Timer
from threading import Thread
import _thread
import pytesseract
import cv2
import numpy as np
from skimage.measure import compare_ssim
import datetime
import logging

class ADB:
    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    DATE_FORMAT = '%Y%m%d %H:%M:%S'
    DATE_TODAY = '{}{}{}'.format(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)
    LOG_FILE = './logs/Logs_{}.log'.format(DATE_TODAY)
    if not os.path.exists(LOG_FILE):
        files = open(LOG_FILE,"w+")
        files.close()
    logging.basicConfig(level=logging.INFO, filename='./logs/Logs_{}.log'.format(DATE_TODAY), format=LOGGING_FORMAT, datefmt=DATE_FORMAT)
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
            logging.error('Error: 請輸入保存圖片的路徑')
            print('wrong!請輸入保存圖片的路徑')
        else:
            var = "\'s/\r$//\'"
            #self.adb_call(device_Name, ['shell', 'screencap', '-p', '/sdcard/screen.jpg'])
            local_path = 'C:/Users/username/python_workspace/GitHub/worldFlipperATS/'+save_path
            self.adb_call(device_Name, ['exec-out', 'screencap', '-p', '>', local_path])
            time.sleep(0.2)
            #self.adb_call(device_Name, ['pull', '/sdcard/screen.jpg', local_path])
            #time.sleep(0.6)
            #self.adb_call(device_Name, ['shell', 'rm', '/sdcard/screen.jpg'])
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
            print('output is : ',output)
            if output != "":
                output = output.split(",")
                end.append(output)
        return end

    def window_capture(self,hwnd,fileName):
        game_Rect = win32gui.GetWindowRect(int(hwnd))
        src_Image = ImageGrab.grab(game_Rect)
        src_Image = src_Image.resize(self,screen_Size,Image.ANTIALIAS)
        src_Image.save(fileName)
        self.screen_Hot = src_Image

    ##position coordinate---
    ##318,458,443,485 account's
    ##470,78,519,110 team-member's 
    ##370,900,442,951 summon-button's
    ##158,582,386,609 setaccount-button
    ##470,26,512,67  delete-button
    ##340,642,437,668  agree-button
    ##111,606,182,629  canceltutorial-button
    ##239,607,291,628  got4starconfirm-button
    ##245,457,290,478  nameconfirm-button
    ##244,663,287,682  accountconfirm-button
    ##176,394,361,481  gotpriceconfirm-button
    ##248,608,287,629  afterpriceconfirmok-button
    ##460,26,503,44  skip-button
    ##434,803,511,854  backtotop-button
    ##----- star(差距66,16)  每一行間角色間距114
    ##79,452,145,468 [0,0]star  193,452,259,468 [0,1]star  307,452,373,468 [0,2]star  421,452,487,468 [0,3]star   1,2,3,4
    ##135,602,201,618 [1,0]star 249,602,315,618 [1,1]star  363,602,429,618 [1,2]star                              5,6,7
    ##79,752,145,768 [2,0]star  193,752,259,768 [2,1]star  307,752,373,768 [2,2]star  451,752,487,768 [2,3]star   8,9,10,11
    ##135,902,201,918 [3,0]star 249,902,315,902 [3,1]star  363,902,429,902 [3,2]star                              12,13,14

    def Image_Grab(self,coordinate=[0,5,0,5],mode=None):
        pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
        tmp_grab_path = r'/image/openCV_Img/'
        path_ = tmp_grab_path+'tmp_grab.jpg'
        self.Game_ScreenHot_By_Adb(save_path=path_)
        img = cv2.imread('.'+path_, cv2.IMREAD_GRAYSCALE)
        count = 1
        if mode == 'get_star':
            coordinate = [[79,452,145,468],[193,452,259,468],[307,452,373,468],[421,452,487,468],
                    [136,602,202,618],[250,602,316,618],[364,602,430,618],
                    [79,752,145,768],[193,752,259,768],[307,752,373,768],[421,752,487,768],
                    [136,902,202,918],[250,902,316,918],[364,902,430,918]
                ]
            for star in coordinate:
                #print('擷取第{}隻'.format(count))
                imgs = img[star[1]:star[3], star[0]:star[2]]
                img_np = np.array(imgs)
                #try:
                frame = cv2.cvtColor(img_np, cv2.cv2.COLOR_BGR2RGB)
                #except:
                #    print('發生錯誤')
                #    self.Image_Grab(mode='get_star')
                #    return 'recognize over'
                cv2.imwrite('.'+tmp_grab_path+str(count)+'.jpg', frame)
                count = count +1
            time.sleep(1)
            return 'recognize over'
        if mode == 'get_account':
            imgs = img[458:485, 318:443] ##[y1::y2, x1:x2]
            img_np = np.array(imgs)
            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            cv2.imwrite('.'+tmp_grab_path+mode+'.jpg', frame)
            result = pytesseract.image_to_string(frame)
            result = re.sub(r'[l\[\]I]','1',result)
            return result
        if mode =='get_summon-button':   ## summon-button
            imgs = img[900:951, 370:442]
        if mode =='get_member-button':  ## member-button
            imgs = img[78:110, 470:519]
        if mode =='get_setaccount-button':  ##158,582,386,609 setaccount-button
            imgs = img[582:609, 158:386]
        if mode =='get_delete-button':  ##470,26,512,67  delete-button
            imgs = img[26:67, 470:512]
        if mode =='get_agree-button':  ##340,642,437,668  agree-button
            imgs = img[642:668, 340:437]
        if mode =='get_canceltutorial-button':  ##111,606,182,629  canceltutorial-button
            imgs = img[606:629, 111:182]
        if mode =='get_nameconfirm-button':  ##245,457,290,478  nameconfirm-button
            imgs = img[458:478, 245:290]
        if mode =='get_gotpriceconfirm-button':  ##176,394,361,481  gotpriceconfirm-button
            imgs = img[394:481, 176:361]
        if mode =='get_afterpriceconfirmok-button':  ##248,608,287,629  afterpriceconfirmok-button
            imgs = img[608:629, 248:287]
        if mode =='get_skip-button':  ##460,26,503,44  skip-button
            imgs = img[26:44, 460:503]
        if mode =='get_backtotop-button':  ##434,803,511,854  backtotop-button
            imgs = img[803:854, 434:511]
        if mode =='get_accountconfirm-button':  ##244,663,287,682  accountconfirm-button
            imgs = img[663:682, 244:287]
        if mode =='get_got4starconfirm-button':  ##239,607,291,628  got4starconfirm-button
            imgs = img[607:628, 239:291]
        img_np = np.array(imgs)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        cv2.imwrite('.'+tmp_grab_path+'checkPoint.jpg', frame)
        if mode is not None and coordinate != [0,5,0,5]:
            imgs = img[coordinate[1]:coordinate[3], coordinate[0]:coordinate[2]]
            img_np = np.array(imgs)
            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            cv2.imwrite('.'+tmp_grab_path+mode+'.jpg', frame)
        #cv2.imwrite(tmp_grab_path+'afterpriceconfirmok-button.jpg', frame) 

    def Recognize_Img(self,mode='None'):
        img_Path = r'./image/openCV_Img/'
        if mode == 'star':
            logging.info('判斷五星角色數量')
            print('開始判斷五星角色數量')
            img_Sample = cv2.imread(img_Path+'five_Star11.png',0)
            starNumber = 0
            for i in range(1,15):
                img_Compare = cv2.imread(img_Path+str(i)+'.jpg',0)
                score = compare_ssim(img_Sample,img_Compare)
                logging.info('第 {} 隻為五星的相似度為 {}%'.format(i,round(score*100,2)))
                print('第 {} 隻為五星的相似度為 {}%'.format(i,round(score*100,2)))
                if score > 0.85:
                    starNumber = starNumber +1
                #print('number_{}\'s score is {}'.format(i,score))
            logging.info('總共抽到 {} 隻五星角色'.format(starNumber))
            print('總共抽到 {} 隻五星角色'.format(starNumber))
            return starNumber
        img_Sample = cv2.imread(img_Path+mode+'.png',0)
        img_Compare = cv2.imread(img_Path+'checkPoint'+'.jpg',0)
        #img_Compare=cv2.resize(img_Compare,img_Sample.shape)
        (H, W) = img_Sample.shape
        # to resize and set the new width and height 
        img_Compare = cv2.resize(img_Compare, (W, H))
        score = compare_ssim(img_Sample,img_Compare)
        if score >= 0.95:
            score = round(score*100,2)
            logging.info('相似度: {}%, 判定成功'.format(score))
            print('相似度: {}%, 判定成功'.format(score))
            return True
        return False


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
        #print(command)
        try:
            subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
            #subprocess.Popen(command,stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as error:
            output = error.output
            code = error.returncode
            #print('the code is :',output)
            if output == b'error: device not found\r\n':
                logging.error(b'error: device not found')
                logging.INFO('執行adb kill-server, 並等待 5 秒重啟時間')
                subprocess.Popen([self.adb_Path,"kill-server"])
                time.sleep(5)
                logging.INFO('重新呼叫command line')
                subprocess.Popen(command,shell=True)
                logging.INFO('重新呼叫成功')

        #subprocess.Popen(command)
        #except 

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