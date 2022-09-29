import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from MyButton import MyButton
from ChessMan import ChessMan
from PyQt5 import QtGui, QtCore
from PyQt5.QtMultimedia import QSound
# 游戏界面类

class GameWeight(QWidget):
    # 定义信号量
    goback_clicked = pyqtSignal()   # 返回信号
    start_clicked = pyqtSignal()    # 开始信号
    regret_clicked = pyqtSignal()   # 悔棋
    lose_clicked = pyqtSignal()     # 认输
    # 鼠标点击落子信号  参数：落子坐标
    position_clicked = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super(GameWeight, self).__init__(parent)
        self.initui()
        # 用于存贮棋子对象 实现悔棋 重新开始 棋子的记录
        self.chessman_list = []
        # 显示输赢图片
        self.winlabel = QLabel(self)
        self.winlabel.hide()    # 图片的隐藏
        # 定义棋子标识
        self.focus = QLabel(self)
        self.focus.setPixmap(QPixmap('source/标识.png'))
        self.focus.setFixedSize(30, 30)
        self.focus.hide()

    # 窗口样式
    def initui(self):
        # 设置标题
        self.setWindowTitle('五子棋游戏')
        # 设置窗口大小
        self.setFixedSize(QImage('source/游戏界面.png').size())
        # 设置背景
        # 获取调色板
        p = QPalette(self.palette())
        # 获取图片
        brush = QBrush(QImage('source/游戏界面.png'))
        # 设置调色板
        p.setBrush(QPalette.Background, brush)
        # 给窗口添加调色板
        self.setPalette(p)
        # 构造控件，设置4个按钮

        # 返回按钮
        self.goback_button = MyButton('source/返回按钮_hover.png',
                                      'source/返回按钮_normal.png',
                                      'source/返回按钮_press.png',
                                      parent=self)
        self.goback_button.move(660, 50)
        self.goback_button.show()
        # 绑定委托
        self.goback_button.click_signal.connect(self.goback_clicked)

        # 开始按钮
        self.start_button = MyButton('source/开始按钮_hover.png',
                                     'source/开始按钮_normal.png',
                                     'source/开始按钮_press.png',
                                     parent=self)
        self.start_button.move(650, 150)
        self.start_button.show()
        # 绑定委托
        self.start_button.click_signal.connect(self.start_clicked)

        # 悔棋按钮
        self.regret_button = MyButton('source/悔棋按钮_hover.png',
                                      'source/悔棋按钮_normal.png',
                                      'source/悔棋按钮_press.png',
                                      parent=self)
        self.regret_button.move(650, 250)
        self.regret_button.show()
        # 绑定委托
        self.regret_button.click_signal.connect(self.regret_clicked)

        # 认输按钮
        self.lose_button = MyButton('source/认输按钮_hover.png',
                                    'source/认输按钮_normal.png',
                                    'source/认输按钮_press.png',
                                    parent=self)
        self.lose_button.move(650, 350)
        self.lose_button.show()
        # 绑定委托
        self.lose_button.click_signal.connect(self.lose_clicked)

    #重新开始
    def reset(self):
        # 清空棋子标识
        self.focus.hide()
        # 清空输赢显示
        self.winlabel.hide()
        # 清空棋子
        for chessman in self.chessman_list:
            chessman.close()

        # 恢复棋盘状态
        self.chessman_list.clear()

    # 悔棋
    def goback(self):
        if len(self.chessman_list) > 0:
            # 删除列表中最后一个元素
            chessman = self.chessman_list.pop()
            chessman.close()
            # 清空棋子标识
            self.focus.hide()

    # 显示游戏输赢
    def show_win(self, color):
        if color == 'black':
            self.winlabel.setPixmap(QPixmap('source/黑棋胜利.png'))
            self.winlabel.show()
            self.winlabel.move(100, 100)
            # 将图片在窗口最上层显示
            self.winlabel.raise_()
        else:
            self.winlabel.setPixmap(QPixmap('source/白棋胜利.png'))
            self.winlabel.show()
            self.winlabel.move(100, 100)
            # 将图片在窗口最上层显示
            self.winlabel.raise_()

    # 获取鼠标点击坐标
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        print('鼠标点击坐标值',a0.x(), a0.y())
        #调用reverse_to_position方法返回棋盘落子位置
        position=self.reverse_to_position(coordinate=a0)
        print('棋盘交点位置为',position)
        # 发射落子信号
        if position is None:
         return
        else:
         self.position_clicked.emit(position)
    # 将鼠标点击坐标转化为棋盘交点坐标
    def reverse_to_position(self,coordinate):
        coor_x=coordinate.x()
        coor_y=coordinate.y()
        #首先判断鼠标位置是否有效，如果无效返回none
        """
        根据棋盘尺寸对落子位置分析
        棋盘上边界y:50-15=35
        棋盘下边界y:50+18*30+15=605
        棋盘左边界x:50-15=35
        棋盘右边界x:50+18*30+15=605
        """
        if coor_x<=35 or coor_x>=605 or coor_y<=35 or coor_y>605:
            return None
        #点击坐标转化为位置坐标
        pos_x=(coor_x-35)//30
        pos_y=(coor_y-35)//30
        return  (pos_x,pos_y)
    #将棋盘交点坐标转化为落子坐标
    def reverse_to_coordinate(self,position):

        #(0,0)
        #落子坐标=坐标原点
        x=50+30*position[0]
        y=50+30*position[1]
        return (x,y)
    # 落子
    def downchess(self, position, color):
        print('执行落子')
        # 构建棋子对象
        chessman = ChessMan(color, self)
        # 点击窗口的位置坐标 确定落子位置
        coorx,coory=self.reverse_to_coordinate(position)
        # 设置棋子的位置，将棋子中心落到棋盘位置
        chessman.move(coorx-15,coory-15) #???
        # 记录棋子对象的交点坐标位置
        chessman.x = position[0]
        chessman.y = position[1]
        # 将新的棋子对象加入到棋子列表里面
        self.chessman_list.append(chessman)
        # 棋子图片展示
        chessman.show()
        # 添加音效
        QSound.play('source/luozisheng.wav')
        # 显示落子标识
        self.focus.move(coorx-15, coory-15)
        self.focus.show()
        self.focus.raise_()

#以下为测试类
def functest():
    print('start......')
class Test(QObject):
    def __init__(self,w):
        super(Test, self).__init__(w)
    def testdown(self,data):
        print('data')
        w.downchess(data,'Black')
if __name__ == '__main__':
    # 创建应用实例
    app = QApplication(sys.argv)
    w = GameWeight()
    w.show()
    #测试开始按钮
    w.start_clicked.connect(functest)
    #测试输赢显示
    w.show_win('black')
    w.downchess((3,3),'Black')
    w.downchess((0,0),'white')
    w.goback()
    w.reset()
    #测试落子，通过鼠标点击坐标
    test_obj=Test(w)
    w.position_clicked.connect(test_obj.testdown)
    sys.exit(app.exec_())

