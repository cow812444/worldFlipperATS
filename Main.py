from GitHub.worldFlipper_ATS.Controller import controller
import time

#package:/data/app/air.jp.co.cygames.worldflipper-1/base.apk=air.jp.co.cygames.worldflipper
#realActivity=air.jp.co.cygames.worldflipper/.AppEntry
class Main:
    def __init__(self):
        self.Controller = controller()

    def Test(self):
        #self.Controller.Game_Start()
        #time.sleep(7)
        #self.Controller.ADB.Touch(662,72)
        self.Controller.ADB.Game_ScreenHot_By_Adb(save_path='test.png')
        self.Controller.ADB.Shut_Down_Game(Game_Activity_Name='air.jp.co.cygames.worldflipper')

        #self.Controller.ADB.Game_ScreenHot_By_Adb()


if __name__ == '__main__':
    ojb = Main()
    ojb.Test()