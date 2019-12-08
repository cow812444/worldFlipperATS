from GameControll import controller
import time

#package:/data/app/air.jp.co.cygames.worldflipper-1/base.apk=air.jp.co.cygames.worldflipper
#realActivity=air.jp.co.cygames.worldflipper/.AppEntry
class Main:
    def __init__(self):
        self.Game_Controller = controller()


    ##79,452,145,468 [0,0]star  193,452,259,468 [0,1]star  307,452,373,468 [0,2]star  421,452,487,468 [0,3]star   1,2,3,4
    ##135,602,201,618 [1,0]star 249,602,315,618 [1,1]star  363,602,429,618 [1,2]star                              5,6,7
    ##79,752,145,768 [2,0]star  193,752,259,768 [2,1]star  307,752,373,768 [2,2]star  421,752,487,768 [2,3]star   8,9,10,11
    ##135,902,201,918 [3,0]star 249,902,315,918 [3,1]star  363,902,429,918 [3,2]star                              12,13,14
    def Testz(self):
        #self.Game_Controller.Game_Start()
        #time.sleep(7)
        #self.Controller.ADB.Touch(662,72)
        self.Game_Controller.ADB.Game_ScreenHot_By_Adb(save_path='test.png')
        position = [307,452,373,468]
        position = [[79,452,145,468],[193,452,259,468],[307,452,373,468],[421,452,487,468],
                    [134,602,200,618],[248,602,314,618],[362,602,428,618],
                    [79,752,145,768],[193,752,259,768],[307,752,373,768],[421,752,487,768],
                    [134,902,200,918],[248,902,314,918],[362,902,428,918]
                ]
        #self.Game_Controller.ADB.Image_Grab(mode='get_afterpriceconfirmok-button')
        #if self.Game_Controller.ADB.Recognize_Img(mode='setaccount-button'):
        #    print('有找到')
        #else:
        #    print('沒找到')
        #self.Controller.ADB.Shut_Down_Game(Game_Activity_Name='air.jp.co.cygames.worldflipper')

        #self.Controller.ADB.Game_ScreenHot_By_Adb()
    def run(self):
        while True:
            self.Game_Controller.Game_Start()   ##開始遊戲
            self.Game_Controller.Delete_Record()  ##刪除紀錄
            self.Game_Controller.Login_Game(achiveTime='firstTime')  ##登入帳號
            self.Game_Controller.Summoning()  ##抽卡
            self.Game_Controller.Game_Stop()  ##關閉遊戲(跳過抽卡動畫)
            self.Game_Controller.Game_Start()  ##開始遊戲
            self.Game_Controller.Login_Game(achiveTime='secondTime')  ##登入帳號
            self.Game_Controller.Check_Box()  #確認包包
            starNumber = self.Game_Controller.Star_Analysis()  ##判斷角色星數
            if starNumber >= 1:
                self.Game_Controller.Get_Account_ID()  ##獲得引繼碼 & 設定密碼
                self.Game_Controller.Recognize_Account(starNumber=starNumber)  ##OCR引繼碼存檔
            self.Game_Controller.Game_Stop()  ##關閉遊戲


if __name__ == '__main__':
    ojb = Main()
    #ojb.Testz()
    ojb.run()