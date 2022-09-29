from PyQt5.QtCore import QObject,pyqtSignal
from GameWeight import  GameWeight
from  GameCore import  GameCore

'''
双人对战模式
'''
class DoublePlayer(QObject):
    exit_clicked=pyqtSignal()
    def __init__(self):
        super(DoublePlayer, self).__init__()
        # 游戏界面
        self.game_weight=GameWeight()
        # 游戏核心对象
        self.game_core=GameCore()
        # 默认棋子颜色
        self.current_color='Black'
        # 定义状态，判断是否可以落子
        self.is_active=False
        # 定义棋子坐标位置
        self.history=[]

        #连接信号与槽函数
        #退出游戏并返回
        self.game_weight.goback_clicked.connect(self.stop_game)
        self.game_weight.start_clicked.connect(self.start_game)
        self.game_weight.regret_clicked.connect(self.regret)
        self.game_weight.lose_clicked.connect(self.lose_game)
        self.game_weight.position_clicked.connect(self.down_chess)
    # 输出相反的棋子颜色
    def get_reverse_color(self,color):
        if color=='Black':
            return 'white'
        else:
            return 'Black'

    #落子逻辑控制
    def down_chess(self,position):
        #判断胜利状态，如果已有输赢显示，无法下棋
        if not self.is_active:
            return
        #判断当前位置是否可以落子
        res=self.game_core.down_chessman(position[0],position[1],self.current_color)
        if res is None:
            return
        #执行实际的界面联系落子逻辑
        self.game_weight.downchess(position,self.current_color)
        #将落子位置进行记录
        self.history.append(position)
        #切换棋子颜色
        self.current_color=self.get_reverse_color(self.current_color)
        #判断输赢状态
        if res != 'Down':
            self.game_weight.show_win(res)
            #重置状态
            self.is_active=False
        #悔棋逻辑
    def regret(self):
        if not self.is_active:
            return
        #判断棋盘中有没有棋子
        if len(self.history)<=0:
           return
        if not self.game_core.regret(*self.history.pop()):
           return
        self.game_weight.goback()
        #悔棋完成更改棋子颜色
        self.current_color=self.get_reverse_color(self.current_color)
        #认输，另一方获胜
    def lose_game(self):
        self.game_weight.show_win(self.get_reverse_color(self.current_color))
        #重置状态
        self.is_active=False
    #游戏初始化
    def init_game(self):
        self.current_color='Black'
        self.game_weight.reset()# 界面初始化
        # 将二维列表重置为空
        self.game_core.init_game()
        self.history.clear()
    # 开始游戏
    def start_game(self):
        #展示游戏界面
        self.game_weight.show()
        self.init_game()
        self.is_active=True
    # 退出游戏
    def stop_game(self):
        print('退出游戏')
        self.exit_clicked.emit()
        self.game_weight.close()