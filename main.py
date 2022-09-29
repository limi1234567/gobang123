import sys
from  MenuWeight import  MenuWeight
from  PyQt5.QtCore import *
from  PyQt5.QtWidgets import *
from  DoublePlayer import  DoublePlayer
from  SinglePlayer import  SinglePlayer
'''
主控程序
'''
class Main(QObject):
    def __init__(self):
        super(Main, self).__init__()
        #初始化菜单界面
        self.menu_weight=MenuWeight()
        #双人对战
        self.double_player=DoublePlayer()
        self.menu_weight.double_clicked.connect(self.start_double_player)
        self.double_player.exit_clicked.connect(self.menu_weight.show)
        #人机对战
        self.single_player=SinglePlayer()
        self.menu_weight.single_clicked.connect(self.start_single_player)
        self.single_player.exit_clicked.connect(self.menu_weight.show)
    #游戏启动方法
    def start_programe(self):
        self.menu_weight.show()#
    def start_double_player(self):
        self.double_player.start_game()
        # 隐藏菜单界面
        self.menu_weight.hide()
    #启动人机对战
    def start_single_player(self):
        self.single_player.start_game()
        self.menu_weight.hide()




if __name__=='__main__':
    app=QApplication(sys.argv)
    main=Main()
    main.start_programe()
    sys.exit(app.exec_())